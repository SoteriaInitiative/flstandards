# User Case Collection
In order to protect the integrity of the effort the specific use case
application is private.

The generic high-level use case is outlined below and follows the guidelines published by [Figma](https://www.figma.com/resource-library/what-is-a-use-case/).

<b>Primary actor:</b> Multiple suspicious activity detection systems

<b>Secondary actor:</b> Compliance officer or law enforcement agency

<b>Goals:</b> Identify suspicious activity of which each individual system has only partial information and privacy of data residing at each system is maintained.

<b>Stakeholders:</b> Regulators, law enforcement, victims and clients

<b>Preconditions:</b> Intelligence sharing among systems in a standardized data format and joint regulatory filing possibility.

<b>Triggers:</b>  Transaction, kyc activity or parts thereof

<b>Scenario:</b> Intelligence (input data and investigation outcome) available
at one system is made available and combined suitably with information
from an other system to increase the likelihood of detection for activity 
that each individual system has limited or no knowledge about. The protocols
and facilities to exchange the locally trained model data, how to combine these
to a global model and then using that information for suspicious activity detection 
comprise the generic use case of this standard.

The illustration below outlines the basic principles of how three financial 
institutions might combined their sheared knowledge about particular threat scenarios
to improve their collective detection capability. Critically, no personal identifiable data
is shared but only abstract matrix data, weights, are shared with the server.

![FedMlIllustration.svg](FedMLIllustration.svg)
