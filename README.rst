Build and push Docker image
---------------------------

.. code-block:: bash

   echo <personal-access-token> | docker login ghcr.io -u tlinhart --password-stdin
   docker build -t ghcr.io/tlinhart/pulumi-aws-python .
   docker push ghcr.io/tlinhart/pulumi-aws-python:latest

Create Pulumi project and stack
-------------------------------

.. code-block:: bash

   export AWS_PROFILE=pasmen
   pulumi login --cloud-url s3://pulumi.linhart.tech
   pulumi new aws-python --dir infra

Provide these values:

- *project name*: pulumi-aws-python
- *project description*: Sample AWS Python Pulumi program
- *stack name*: pulumi-aws-python-prod
- *passphrase*: <secret-passphrase>
- *aws:region*: eu-central-1

.. code-block:: bash

   export PULUMI_CONFIG_PASSPHRASE=<secret-passphrase>
   cd infra
   pulumi config set aws:profile pasmen
   pulumi config set ghcr-token <personal-access-token> --secret

Manage the stack
----------------

- ``pulumi up`` - Create or update the resources in a stack
- ``pulumi stack output [<property-name>]`` - Show a stack's output properties
- ``pulumi destroy`` - Destroy an existing stack and its resources
- ``pulumi stack rm [<stack-name>]`` - Remove a stack and its configuration

Access the web server
---------------------

.. code-block:: bash

   curl $(pulumi stack output public_ip):5000

Resources
---------

- https://www.pulumi.com/docs/get-started/aws/
- https://github.com/pulumi/examples/tree/master/aws-py-webserver
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts
- https://stackoverflow.com/a/9766919/5832540
