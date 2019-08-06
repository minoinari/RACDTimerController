#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file RACDTimerController.py
 @brief Joystick to robot, arm, camera and display(Timer) and stop the robot movement when time's up
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
racdtimercontroller_spec = ["implementation_id", "RACDTimerController", 
		 "type_name",         "RACDTimerController", 
		 "description",       "Joystick to robot, arm, camera and display(Timer) and stop the robot movement when time's up", 
		 "version",           "1.0.0", 
		 "vendor",            "m.toyoda", 
		 "category",          "Controller", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.speed_x", "0.1",
		 "conf.default.speed_r", "0.5",

		 "conf.__widget__.speed_x", "slider.0.01",
		 "conf.__widget__.speed_r", "slider.0.01",
		 "conf.__constraints__.speed_x", "-2.0<x<2.0",
		 "conf.__constraints__.speed_r", "-2.0<x<2.0",

         "conf.__type__.speed_x", "double",
         "conf.__type__.speed_r", "double",

		 ""]
# </rtc-template>

##
# @class RACDTimerController
# @brief Joystick to robot, arm, camera and display(Timer) and stop the robot movement when time's up
# 
# 
class RACDTimerController(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		"""
		Joy stickからの入力
		それぞれのボタンの情報がboolの配列で
		"""
		self._d_in = OpenRTM_aist.instantiateDataType(RTC.TimedBooleanSeq)
		self._inIn = OpenRTM_aist.InPort("in", self._d_in)
		"""
		終わったらTrueが返ってくる
		"""
		self._d_stop = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		self._stopIn = OpenRTM_aist.InPort("stop", self._d_stop)
		"""
		前後進と左右
		m/s, rad/s
		"""
		self._d_vel = OpenRTM_aist.instantiateDataType(RTC.TimedVelocity2D)
		self._velOut = OpenRTM_aist.OutPort("vel", self._d_vel)
		"""
		armのopen/close
		"""
		self._d_arm = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		self._armOut = OpenRTM_aist.OutPort("arm", self._d_arm)
		"""
		camera 1 or 2
		"""
		self._d_camera = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		self._cameraOut = OpenRTM_aist.OutPort("camera", self._d_camera)
		"""
		距離表示 あり or なし
		"""
		self._d_display = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		self._displayOut = OpenRTM_aist.OutPort("display", self._d_display)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		移動速度
		 - Name: speed_x speed_x
		 - DefaultValue: 0.1
		"""
		self._speed_x = [0.1]
		"""
		回転速度
		 - Name: speed_r speed_r
		 - DefaultValue: 0.5
		"""
		self._speed_r = [0.5]
		
		# </rtc-template>

		# flags
		self.arm_open = True
		self.camera_1 = False
		self.display_on = True

		# joystick button
		self.fo_num = 3  # for forward
		self.ba_num = 2  # for back
		self.ri_num = 7  # for turn right
		self.le_num = 6  # for turn left

		self.ar_num = 5  # for arm
		self.ca_num = 4  # for camera
		self.di_num = 0  # for display


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("speed_x", self._speed_x, "0.1")
		self.bindParameter("speed_r", self._speed_r, "0.5")
		
		# Set InPort buffers
		self.addInPort("in",self._inIn)
		self.addInPort("stop",self._stopIn)
		
		# Set OutPort buffers
		self.addOutPort("vel",self._velOut)
		self.addOutPort("arm",self._armOut)
		self.addOutPort("camera",self._cameraOut)
		self.addOutPort("display",self._displayOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	###
	## 
	## The finalize action (on ALIVE->END transition)
	## formaer rtc_exiting_entry()
	## 
	## @return RTC::ReturnCode_t
	#
	## 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The startup action when ExecutionContext startup
	## former rtc_starting_entry()
	## 
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The shutdown action when ExecutionContext stop
	## former rtc_stopping_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	##
	#
	# The activated action (Active state entry action)
	# former rtc_active_entry()
	#
	# @param ec_id target ExecutionContext Id
	# 
	# @return RTC::ReturnCode_t
	#
	#
	def onActivated(self, ec_id):
		self.arm_open = False
		self.camera_1 = False
		self.display_on = False
		self.a_onoff = True
		self.c_onoff = True
		self.d_onoff = True

		self.game = False

		return RTC.RTC_OK
	
	##
	#
	# The deactivated action (Active state exit action)
	# former rtc_active_exit()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	

	
	def changeState(self, in_button, pre, out_data, outport_data, onoff):
		
		if self._in.data[in_button] != pre:  # if the signal is changed, change a signal
			if onoff:
				if out_data == True:
					out_data = False
					#print("2")
					#print(out_data)
				else:
					out_data = True
					#print("1")
					#print(out_data)
				onoff = False
			else:
				onoff = True

		return out_data, onoff

	##
	#
	# The execution action that is invoked periodically
	# former rtc_active_do()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onExecute(self, ec_id):
		if self._inIn.isNew():
			self._in = self._inIn.read()
			if self._stopIn.isNew():
				self._stop = self._stopIn.read()
				if self._stop:
					self.game = False

					# robot stop
					self._d_vel.data.vx = 0
					self._d_vel.data.va = 0
					self._velOut.write()					
			#print(self.game)
			
			if self.game:
				
				#########################
				##### velocity, arc #####
				#########################

				self._d_vel.data.vy = 0
				
				if self._in.data[self.fo_num]:  # forward  (button "4"(you can change this number in __init__))
					self._d_vel.data.vx = -1 * self._speed_x[0]
				elif self._in.data[self.ba_num]:  # back  (button "3"(you can change this number in __init__))
					self._d_vel.data.vx = 1 * self._speed_x[0]
				elif not(self._in.data[self.fo_num]) and not(self._in.data[self.ba_num]):
					self._d_vel.data.vx = 0

				if self._in.data[self.ri_num]: # turn right  (button "7")
					self._d_vel.data.va = -1 * self._speed_r[0]
				elif self._in.data[self.le_num]:  # turn left  (button "6")
					self._d_vel.data.va = 1 * self._speed_r[0]
				elif not(self._in.data[self.ri_num]) and not(self._in.data[self.le_num]):
					self._d_vel.data.va = 0

				self._velOut.write()

				
				#########################
				########## arm ##########
				#########################
				
				self._d_arm.data, self.a_onoff = self.changeState(self.ar_num, self.arm_open, self._d_arm.data, self._armOut, self.a_onoff)
				if self._in.data[self.ar_num] != self.arm_open:
					if not(self.a_onoff):
						self._armOut.write()
						#print("OK")
				self.arm_open = self._in.data[self.ar_num]


				#########################
				######## camera #########
				#########################
				
				self._d_camera.data, self.c_onoff = self.changeState(self.ca_num, self.camera_1, self._d_camera.data, self._cameraOut, self.c_onoff)
				if self._in.data[self.ca_num] != self.camera_1:
					if not(self.c_onoff):
						self._cameraOut.write()
				self.camera_1 = self._in.data[self.ca_num]


			#########################
			##### display(timer) ####
			#########################

			self._d_display.data, self.d_onoff = self.changeState(self.di_num, self.display_on, self._d_display.data, self._displayOut, self.d_onoff)
			if self._in.data[self.di_num] != self.display_on:
				if not(self.d_onoff):
					self._displayOut.write()
					self.game = True
			self.display_on = self._in.data[self.di_num]

		return RTC.RTC_OK
	
	###
	##
	## The aborting action when main logic error occurred.
	## former rtc_aborting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The error action in ERROR state
	## former rtc_error_do()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The reset action that is invoked resetting
	## This is same but different the former rtc_init_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The state update action that is invoked after onExecute() action
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##

	##
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The action that is invoked when execution context's rate is changed
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def RACDTimerControllerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=racdtimercontroller_spec)
    manager.registerFactory(profile,
                            RACDTimerController,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    RACDTimerControllerInit(manager)

    # Create a component
    comp = manager.createComponent("RACDTimerController")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

