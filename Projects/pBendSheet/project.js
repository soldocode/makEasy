
var material_handler=new THREE.MeshLambertMaterial({color: 0x666666, transparent: true, opacity:0.2});

function makeObject(id)
    {
     var thk=15
     var group = new THREE.Object3D();
     group.add(makeSegment(150,thk,0,0,0))
     //group.add(makeSegment(100,thk,150,0,0.7))

     group.add(makeHandler(thk,150,7.5))
     group.add(makeHandler(thk,0,7.5))

     objects[id]={"element":group}
     return group;
    }

function makeHandler(thk,x,y)
    {
        var result=new THREE.Mesh(new THREE.SphereGeometry( thk/2, 24, 24 ),material_handler)
        result.position.set(x, y, 0);
        return result
    }

function makeSegment(length,thk,x,y,angle)
    {
        var result=new THREE.Object3D();
        var shape = new THREE.Shape();
        shape.moveTo( 0,0 );
        shape.lineTo( length,0  );
        shape.lineTo( length,thk );
        shape.lineTo( 0,thk  );
        shape.lineTo( 0,0 );

        //pShape=make_rect(lenght,50);
        //sPath=make_rect_path(lenght,10);
        result.add(new THREE.Line(shape.createPointsGeometry(),lineMaterial));
        var options = {
                        amount: -1,
                        steps: 1,
                        bevelSegments: 0,
                        bevelSize: 0,
                        bevelThickness: 0
                      };
        result.add(new THREE.Mesh(new THREE.ExtrudeGeometry(shape, options),material));
        result.rotation.z=angle;
        result.position.set(x, y, 0);
        return result
    }

function makeBend(thk,angleStart,angleEnd,radius,x,y)
    {
        var result=new THREE.Object3D();
        var path=new THREE.Path();
        //path.moveTo(0,0);
        path.arc ( 0, 0, radius, angleStart, angleEnd, false );
        path.arc ( 0, 0, radius+thk, angleStart, angleEnd, true );
        //path.lineTo(0,0);
        var geometry = path.makeGeometry();
        var shape=path.toShapes();
        result.add(new THREE.Line(geometry,lineMaterial));
        var options = {
                        amount: -1,
                        steps: 1,
                        bevelSegments: 0,
                        bevelSize: 0,
                        bevelThickness: 0
                      };
        result.add(new THREE.Mesh(new THREE.ExtrudeGeometry(shape, options),material));
        return result
    }

function update_shape()
    {
     if (objects.project){scene.remove(objects.project.element)}

     makeObject('project');
     scene.add(objects.project.element);
    }


$(".value").on("change",update_shape);
camera.position.set(0,0,8000);
camera.up.set(0,1,0);
camera.updateProjectionMatrix ();
cameraControls.noRotate=true;
cameraControls.update();

