# -*- coding: utf-8 -*-

#Simple example Robot Raconteur Industrial Cognex service

import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
from RobotRaconteurCompanion.Util.UuidUtil import UuidUtil
from RobotRaconteurCompanion.Util.IdentifierUtil import IdentifierUtil
from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil
from RobotRaconteurCompanion.Util.SensorDataUtil import SensorDataUtil
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
from RobotRaconteurCompanion.Util.RobDef import register_service_types_from_resources
import drekar_launch_process
import argparse
import numpy as np
import socket, threading, traceback, copy, time, os, signal

host = '0.0.0.0'		#IP address of PC
port = 3000



def multisplit(s, delims):
	pos = 0
	for i, c in enumerate(s):
		if c in delims:
			yield s[pos:i]
			pos = i + 1
	yield s[pos:]


class sensor_impl(object):
	def __init__(self, object_sensor_info):

		self.object_recognition_sensor_info = object_sensor_info
		self.device_info = object_sensor_info.device_info

		#initialize socket connection
		self.s=socket.socket()
		self.s.bind((host, port))
		self.s.listen(5)		

		#threading setting
		self._lock=threading.RLock()
		self._running=False

		#utils
		self._uuid_util=UuidUtil(RRN)
		self._identifier_util=IdentifierUtil(RRN)
		self._geometry_util=GeometryUtil(RRN)
		self._sensor_data_util=SensorDataUtil(RRN)
		
		#initialize objrecog types
		self._object_recognition_sensor_data_type = RRN.GetStructureType("com.robotraconteur.objectrecognition.ObjectRecognitionSensorData")
		self._recognized_objects_type = RRN.GetStructureType("com.robotraconteur.objectrecognition.RecognizedObjects")

		self._recognized_object_type=RRN.GetStructureType("com.robotraconteur.objectrecognition.RecognizedObject")
		self._named_pose_cov_type=RRN.GetStructureType("com.robotraconteur.geometry.NamedPoseWithCovariance")
		self._named_pose_type = RRN.GetStructureType("com.robotraconteur.geometry.NamedPose")
		

		#initialize detection obj map
		self._detection_obj_type=RRN.NewStructure("edu.robotraconteur.cognexsensor.detection_obj")

		self._seqno = 0
		self._detected_objects = None
		self._wires_init = False

	def RRServiceObjectInit(self, ctx, service_path):
		self._wires_init = True
		
	def start(self):
		self._running=True
		self._camera = threading.Thread(target=self._object_update)
		self._camera.daemon = True
		self._camera.start()
	def close(self):
		self._running = False
		try:
			self.s.close()
		except:
			pass
		try:
			self.c.close()
		except:
			pass
		self._camera.join()

	def parse_sensor_string(self, string_data):

		recognized_objects = []
		detected_objects = {}

		string_data=string_data.split('{')			#find leading text
		object_list = string_data[-1].split(";")	# split different object info in string
		object_list.pop(0)

		for i in range(len(object_list)):  					# split the data from cognex and parse to RR object
			general = object_list[i].split(":")	
			name=general[0]
			if '#ERR' not in general[1]:			#if detected
				
				info = list(filter(None, multisplit(general[1], '(),=°\r\n')))
				#standard type

				recognized_object = self._recognized_object_type()
				recognized_object.recognized_object = self._identifier_util.CreateIdentifierFromName(name)
				named_pose = self._named_pose_type()
				named_pose.pose = self._geometry_util.xyz_rpy_to_pose([float(info[0])/1000., float(info[1])/1000., 0.0], [0.0, 0.0, np.deg2rad(float(info[2]))])
				cov_pose = self._named_pose_cov_type()
				cov_pose.pose = named_pose
				recognized_object.pose = cov_pose
				recognized_object.confidence = float(info[3])/100.
				recognized_objects.append(recognized_object)
				
				#my type
				detected_object = self._detection_obj_type
				detected_object.name = name
				detected_object.x = float(info[0])/1000.
				detected_object.y = float(info[1])/1000.
				detected_object.angle = float(info[2])
				detected_object.detected = True
				detected_objects[name] = detected_object

		recognized_objects_sensor_data = self._object_recognition_sensor_data_type()
		recognized_objects_sensor_data.sensor_data = self._sensor_data_util.FillSensorDataHeader(self.device_info, self._seqno)
		recognized_objects_sensor_data.recognized_objects = self._recognized_objects_type()
		recognized_objects_sensor_data.recognized_objects.recognized_objects = recognized_objects

		self._seqno += 1

		return recognized_objects_sensor_data, detected_objects

	def _object_update(self):

		connected = False
		self.c = None

		while self._running:

			if not connected:
				try:
					self.c, addr = self.s.accept()
					connected = True
					print("Connected to Cognex sensor")
				except:
					time.sleep(0.5)
					continue
			
			if not self._running:
				break

			try:
				string_data = self.c.recv(1024).decode("utf-8")
				if len(string_data) == 0:
					if connected:
						connected = False
						try:
							self.c.close()
						except:
							pass
						print("Warning: Connection to Cognex sensor lost")				
			except:
				if connected:
					connected = False
					try:
						self.c.close()
					except:
						pass
					print("Warning: Connection to Cognex sensor lost")
				time.sleep(0.5)
				continue

			if not self._running:
				break

			try:
				object_recognition_sensor_data, detection_objects = self.parse_sensor_string(string_data)

				with self._lock:
					self._detected_objects = object_recognition_sensor_data.recognized_objects
					
				if self._wires_init:
					#pass to RR wire
					self.detection_wire.OutValue=detection_objects
					#pass to RR pipe
					self.object_recognition_sensor_data.SendPacket(object_recognition_sensor_data)
			except:
				traceback.print_exc()

		try:
			self.c.close()
		except:
			pass

	def capture_recognized_objects(self):
		with self._lock:
			if self._detected_objects is None:
				ret = self._recognized_objects_type()
				ret.recognized_objects = []
				return ret
			return copy.deepcopy(self._detected_objects)

def main():

	parser = argparse.ArgumentParser(description="Cognex Sensor Robot Raconteur Driver")

	parser.add_argument("--sensor-info-file", type=argparse.FileType('r'),default=None,required=True,help="Cognex sensor info file (required)")

	args, _ = parser.parse_known_args()

	RRC.RegisterStdRobDefServiceTypes(RRN)
	register_service_types_from_resources(RRN, __package__, ['edu.robotraconteur.cognexsensor.robdef'])

	with args.sensor_info_file:
		sensor_info_text = args.sensor_info_file.read()

	info_loader = InfoFileLoader(RRN)
	sensor_info, sensor_ident_fd = info_loader.LoadInfoFileFromString(sensor_info_text, \
                                            "com.robotraconteur.objectrecognition.ObjectRecognitionSensorInfo", "device")
	
	attributes_util = AttributesUtil(RRN)
	sensor_attributes = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(sensor_info.device_info)
    


	with RR.ServerNodeSetup("cognex_Service", 59901) as node_setup:

		cognex_inst=sensor_impl(sensor_info)
		cognex_inst.start()

		ctx = RRN.RegisterService("cognex", "edu.robotraconteur.cognexsensor.CognexSensor", cognex_inst)
		ctx.SetServiceAttributes(sensor_attributes)

		print("Cognex Service Started")
		print()
		print("Candidate connection urls:")
		ctx.PrintCandidateConnectionURLs()
		print()
		print("Press Ctrl-C to quit...")

		drekar_launch_process.wait_exit()
		
		cognex_inst.close()
