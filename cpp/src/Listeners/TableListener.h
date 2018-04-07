#pragma once

using namespace boost::python; 

class TableListener : public IO2GTableListener
{
public:
	virtual void onAdded(const char *rowID, IO2GRow *rowData) = 0;
	virtual void onChanged(const char *rowID, IO2GRow *rowData) = 0;
	virtual void onDeleted(const char *rowID, IO2GRow *rowData) = 0;
	virtual void onStatusChanged(O2GTableStatus status) = 0;
	virtual long addRef() = 0;
	virtual long release() = 0;
};

class gil_lock
{
public:
  gil_lock()  { state_ = PyGILState_Ensure(); }

  ~gil_lock() { PyGILState_Release(state_);   }

private:
  PyGILState_STATE state_;
};

class TableListenerImpl : public TableListener 
{
public:
	TableListenerImpl(PyObject* pyObject) : self(pyObject){}
	TableListenerImpl(PyObject* pyObject, const TableListener& listener) : self(pyObject), TableListener(listener){}

	void onAdded(const char *rowID, IO2GRow *rowData) 
	{
                gil_lock lock;
                try
                {
                        call_method<void>(self, "_on_added", rowID, boost::ref(rowData));
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	};

	void onChanged(const char *rowID, IO2GRow *rowData)
	{
                gil_lock lock;
                try
                {
                        call_method<void>(self, "_on_changed", rowID, boost::ref(rowData));
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	};
	void onDeleted(const char *rowID, IO2GRow *rowData)
	{
                gil_lock lock;
                try
                {
                        call_method<void>(self, "_on_deleted", rowID, boost::ref(rowData));
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	};
	void onStatusChanged(O2GTableStatus status)
	{
                gil_lock lock;
                try
                {
                        call_method<void>(self, "_on_status_changed", status);
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	};
	long addRef()
	{
                gil_lock lock;
                try
                {
                        long refCount = call_method<long>(self, "addRef");
                        return refCount;
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	}

	long release()
	{
                gil_lock lock;
                try
                {
                        long refCount = call_method<long>(self, "release");
                        return refCount;
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	}

private:
	PyObject* const self;
};