# Exceptions

### *exception* ots.exceptions.OtsException(error)

Wraps the OTS error into an Exception with a message.

#### code() → int

* **Returns:**
  The code of the error.

#### error_class() → str

* **Returns:**
  The class of the error.

#### message() → str

* **Returns:**
  The message of the error.

#### *static* from_result(result: [ots_result_t](raw.md#ots.raw.ots_result_t) | \_CDataBase) → [OtsException](#ots.exceptions.OtsException)

Creates an OtsException from a result object.
