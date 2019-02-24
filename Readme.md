| **URL EndPoint**          | **HTTP Method**| **Public Access** | **Summary**                            |
| ------------------------  | ---------------| ----------------- |----------------------------------------|
| complaint/str:pk/         |     PUT        |      False        | Update a complaint(complainant only)   |
| complaint/str:pk/         |     GET        |      False        | Get a complaint(complainant only)      |
| complaint/str:pk/         |  DELETE        |      False        | Delete a complaint(complainant only)   |
| create-complaint/         |  POST          |      False        | Create a complaint(complainant only)   |
| complaints/               |  GET           |      False        | View all open complaints(lawyer only)  |
|accept-complaint/str:id/   |  POST          |      False        | Add a complaint to a lawyer            |
|complaints/str:id/         |  GET           |      False        | Retrieve a complaint(lawyer only)      |