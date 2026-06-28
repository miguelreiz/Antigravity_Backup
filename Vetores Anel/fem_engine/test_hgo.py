import subprocess

xml = '''<?xml version="1.0" encoding="UTF-8"?>
<febio_spec version="4.0">
  <Module type="solid"/>
  <Control>
    <analysis>STATIC</analysis>
    <time_steps>1</time_steps>
    <step_size>1</step_size>
    <solver type="solid"/>
  </Control>
  <Material>
    <material id="1" name="Cornea" type="Holzapfel-Gasser-Ogden">
      <c>0.01</c><k1>10.0</k1><k2>100.0</k2><kappa>0.2</kappa><gamma>0.0</gamma><k>100.0</k>
    </material>
  </Material>
  <Mesh>
    <Nodes name="n"><node id="1">0,0,0</node><node id="2">1,0,0</node><node id="3">1,1,0</node><node id="4">0,1,0</node><node id="5">0,0,1</node><node id="6">1,0,1</node><node id="7">1,1,1</node><node id="8">0,1,1</node></Nodes>
    <Elements type="hex8" name="p" mat="1"><elem id="1">1,2,3,4,5,6,7,8</elem></Elements>
  </Mesh>
  <MeshDomains>
    <SolidDomain name="p" mat="Cornea"/>
  </MeshDomains>
  <MeshData>
    <ElementData name="mat_axis" elem_set="p">
      <e lid="1">
        <a>1,0,0</a>
        <d>0,1,0</d>
      </e>
    </ElementData>
  </MeshData>
</febio_spec>'''

with open('test_hgo.feb', 'w') as f: f.write(xml)
res = subprocess.run([r'C:\Program Files\FEBioStudio\bin\febio4.exe', '-i', 'test_hgo.feb'], capture_output=True, text=True)
print([line for line in res.stdout.split('\n') if 'ERROR' in line or 'FAILED' in line or 'missing' in line or 'invalid' in line])
