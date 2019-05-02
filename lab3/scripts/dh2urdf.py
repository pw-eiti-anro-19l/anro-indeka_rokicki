#! /usr/bin/python

import json

if __name__ == '__main__':
    params = {}
    results = ''
    with open('../dh.json', 'r') as file:
        params = json.loads(file.read())

    with open('../urdf.yaml', 'w') as file:
        for key in params.keys():
            a, d, al, th = params[key]
            a, d, al, th = float(a), float(d), float(al), float(th)

	    xyz=[a, 0, 0]

	    if al!=0:
		if al>0:
		    xyz[1]=-d
		    if th>0:
			rpy=[al, -th, 0]
		    elif th<0:
			rpy=[al, th, 0]
		    else:
			rpy=[al, 0, 0]
		else:
		    xyz[1]=d
		    if th>0:
			rpy=[-al, th, 0]
		    elif th<0:
			rpy=[-al, -th, 0]
		    else:
			rpy=[-al, 0, 0]
	    else:
		xyz[2]=d
		if th>0:
		    rpy=[0, 0, th]
		elif th<0:
		    rpy=[0, 0, -th]
		else:
		    rpy=[0, 0, 0]


            file.write(key + ":\n")
            file.write("  j_xyz: {} {} {}\n".format(xyz[0],xyz[1],xyz[2]))
            file.write("  j_rpy: {} {} {}\n".format(rpy[0],rpy[1],rpy[2]))
            file.write("  l_xyz: {} {} {}\n".format(0, 0, -d/2))
            file.write("  l_rpy: {} {} {}\n".format(0,0,0))
            file.write("  l_len: {}\n".format(d))
