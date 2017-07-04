
var material_handler=new THREE.MeshLambertMaterial({color: 0x666666, transparent: true, opacity:0.1});

function radians(degree)
    {
        return degree * Math.PI / 180
    }

function makeObject(id)
    {

     // get parameters
     var thk=parseFloat($("input[name='thickness:number']").val());
     var sLen=parseFloat($("input[name='lenght:number']").val());


     //var thk=15
     var group = new THREE.Object3D();
     group.add(makeSegment(150,thk,0,0,0,sLen))
     //group.add(makeSegment(100,thk,150,0,0.7))

     group.add(makeHandler(thk,150,7.5))
     group.add(makeHandler(thk,0,7.5))
     group.add(makeBend(thk,270,0,10,150,0,sLen))
     group.add(makeBend(thk,90,180,4,0,thk,sLen))

     objects[id]={"element":group}
     return group;
    }

function makeHandler(thk,x,y)
    {
        var result=new THREE.Mesh(new THREE.SphereGeometry( thk/2, 24, 24 ),material_handler)
        result.position.set(x, y, 0);
        return result
    }

function makeSegment(length,thk,x,y,angle,sLen)
    {
        var result=new THREE.Object3D();
        var shape = new THREE.Shape();
        shape.moveTo( 0,0 );
        shape.lineTo( length,0  );
        shape.lineTo( length,thk );
        shape.lineTo( 0,thk  );
        shape.lineTo( 0,0 );

        result.add(new THREE.Line(shape.createPointsGeometry(),lineMaterial));
        var options = {
                        amount: sLen,
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


function makeBend(thk,angleStart,angleEnd,radius,x,y,sLen)
    {
        var result=new THREE.Object3D();
        var path=new THREE.Path();
        path.moveTo(0,0);
        path.absarc (0,0, radius, radians(angleStart), radians(angleEnd) , false );
        path.absarc (0,0, radius+thk, radians(angleEnd), radians(angleStart), true );
        path.closePath();

        var geometry = path.createPointsGeometry();
        result.add(new THREE.Line(geometry,lineMaterial));

        var shape = new THREE.Shape(geometry.vertices);
        var options = {
                        amount: sLen,
                        steps: 1,
                        bevelSegments: 0,
                        bevelSize: 0,
                        bevelThickness: 0
                      };
        result.add(new THREE.Mesh(new THREE.ExtrudeGeometry(shape, options),material_handler));
        oX=(radius+thk)*Math.cos(radians(angleStart))
        oY=(radius+thk)*Math.sin(radians(angleStart))
        console.log(oX,oY);
        result.position.set(x-oX,y-oY,0);
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
//cameraControls.noRotate=true;
cameraControls.update();

