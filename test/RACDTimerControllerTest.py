#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file RACDTimerControllerTest.py
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
racdtimercontrollertest_spec = ["implementation_id", "RACDTimerControllerTest", 
		 "type_name",         "RACDTimerControllerTest", 
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
# @class RACDTimerControllerTest
# @brief Joystick to robot, arm, camera and display(Timer) and stop the robot movement when time's up
# 
# 
class RACDTimerControllerTest(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_vel = OpenRTM_aist.instantiateDataType(RTC.TimedVelocity2D)
		"""
		前後進と左右
		"""
		self._velIn = OpenRTM_aist.InPort("vel", self._d_vel)
		self._d_arm = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		armのopen/close
		"""
		self._armIn = OpenRTM_aist.InPort("arm", self._d_arm)
		self._d_camera = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		camera 1 or 2
		"""
		self._cameraIn = OpenRTM_aist.InPort("camera", self._d_camera)
		self._d_display = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		距離表示 あり or なし
		"""
		self._displayIn = OpenRTM_aist.InPort("display", self._d_display)
		self._d_in = OpenRTM_aist.instantiateDataType(RTC.TimedBooleanSeq)
		"""
		Joy stickからの入力
		それぞれのボタンの情報がboolの配列で
		"""
		self._inOut = OpenRTM_aist.OutPort("in", self._d_in)
		self._d_stop = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		終わったらTrueが返ってくる
		"""
		self._stopOut = OpenRTM_aist.OutPort("stop", self._d_stop)


		


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
		self.addInPort("vel",self._velIn)
		self.addInPort("arm",self._armIn)
		self.addInPort("camera",self._cameraIn)
		self.addInPort("display",self._displayIn)
		
		# Set OutPort buffers
		self.addOutPort("in",self._inOut)
		self.addOutPort("stop",self._stopOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
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
	
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def RACDTimerControllerTestInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=racdtimercontrollertest_spec)
    manager.registerFactory(profile,
                            RACDTimerControllerTest,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    RACDTimerControllerTestInit(manager)

    # Create a component
    comp = manager.createComponent("RACDTimerControllerTest")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

