# Charge Live Status (POC)


## OCPP References
### StatusNotification Request
| Field Name      | Field Type | Required | Description |
| --- | --- | --- | --- |
| connectorId     | integer connectorId >= 0 | true | The id of the connector for which the status is reported. Id '0' (zero) is used if the status is for the Charge Point main controller. |
| errorCode       | ChargePointErrorCode | true | This contains the error code reported by the Charge Point. |
| info            | CiString50Type | false | Additional free format information related to the error. | 
| status          | ChargePointStatus | true | This contains the current status of the Charge Point. |
| timestamp       | dateTime | false | The time for which the status is reported. If absent time of receipt of the message will be assumed. |
| vendorId        | CiString255Type | false | This identifies the vendor-specific implementation. |
| vendorErrorCode | CiString50Type | false | This contains the vendor-specific error code. |

### Sample Charging StatusNotification Request
```json
{
  "connector_id": 1, 
  "error_code": "NoError", 
  "status": "Charging", 
  "timestamp": "2023-01-01T09:00:00Z", 
  "info": null, 
  "vendor_id": null, 
  "vendor_error_code": null
}
```


### ChargePointErrorCode
| Value  | Description |
| --- | --- |
| ConnectorLockFailure | Failure to lock or unlock connector. |
| EVCommunicationError  | Communication failure with the vehicle, might be Mode 3 or other communication protocol problem. This is not a real error in the sense that the Charge Point doesn’t need to go to the faulted state. Instead, it should go to the SuspendedEVSE state. |
| GroundFailure | Ground fault circuit interrupter has been activated. |
| HighTemperature  | Temperature inside Charge Point is too high. |
| InternalError  | Error in internal hard- or software component. |
| LocalListConflict  | The authorization information received from the Central System is in conflict with the LocalAuthorizationList. |
| NoError  | No error to report. |
| OtherError | Other type of error. More information in vendorErrorCode. |
| OverCurrentFailure | Over current protection device has tripped. |
| OverVoltage  | Voltage has risen above an acceptable level. |
| PowerMeterFailure  | Failure to read power meter. |
| PowerSwitchFailure  | Failure to control power switch. |
| ReaderFailure  | Failure with idTag reader. |
| ResetFailure  | Unable to perform a reset. |
| UnderVoltage  | Voltage has dropped below an acceptable level. |
| WeakSignal  | Wireless communication device reports a weak signal. |

### Charge Point Status
| Status | Operative | Condition |
| --- |-----------| --- |
| Available | true      | When a Connector becomes available for a new user |
| Preparing | true      | When a Connector becomes no longer available for a new user but no charging session is active. Typically a Connector is occupied when a user presents a tag, inserts a cable or a vehicle occupies the parking bay |
| Charging | true      | When the contactor of a Connector closes, allowing the vehicle to charge |
| SuspendedEVSE | true      | When the contactor of a Connector opens upon request of the EVSE, e.g. due to a smart charging restriction or as the result of StartTransaction.conf indicating that charging is not allowed |
| SuspendedEV | true      | When the EVSE is ready to deliver energy but contactor is open, e.g. the EV is not ready. |
| Finishing  | true      | When a charging session has stopped at a Connector, but the Connector is not yet available for a new user, e.g. the cable has not been removed or the vehicle has not left the parking bay. |
| Reserved  | true      | When a Connector becomes reserved as a result of a Reserve Now command |
| Unavailable  | false     | When a Connector becomes unavailable as the result of a Change Availability command or an event upon which the Charge Point transitions to unavailable at its discretion. Upon receipt of a Change Availability command, the status MAY change immediately or the change MAY be scheduled. When scheduled, the Status Notification shall be send when the availability change becomes effective |
| Faulted | false     | When a Charge Point or connector has reported an error and is not available for energy delivery. |