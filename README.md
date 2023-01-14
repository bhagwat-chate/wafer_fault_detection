# PoC-sensor-fault-detection

### Problem Statement
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the break pads, showing the vehicle down. The benefits of using an APS instead of hydraulic system are the easy availability and long-term sustainability of nutural air.

This is a Binary Classification business statement, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class indicates that the failure was caused by something else.

### Proposed Solution
In this project, the system in focus is the Air Pressure System (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class correspond failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The business statement is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

### Tech Stack Used
1. Python
2. FastAPI
3. Maching Learning algorithm
4. Docker
5. MongoDB

### Infrastructure Required
1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions
5. Terraform
