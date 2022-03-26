Create a secrets.yaml file like this:

<pre>
apiVersion: v1
kind: Secret
metadata:
  name: opal-passwords
type: Opaque
data:
  POSTGRES_OPAL_PASSWORD: ***************
  POSTGRES_PASSWORD: ****************
</pre>


Then run kubectl apply -f . from this directory