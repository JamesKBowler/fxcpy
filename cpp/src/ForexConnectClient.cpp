// Defines the exported functions for the application.
//

#include "stdafx.h"
#include "ForexConnectClient.h"

// This is an example of an exported variable
FOREXCONNECT_API int nforexconnect=0;

// This is an example of an exported function.
FOREXCONNECT_API int fnforexconnect(void)
{
	return 42;
}

// This is the constructor of a class that has been exported.
// see forex.connect.h for the class definition
Cforexconnect::Cforexconnect()
{
	return;
}