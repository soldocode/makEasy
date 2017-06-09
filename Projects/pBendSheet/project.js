
function makeObject(id)
    {
     var thk=5
     var group = new THREE.Object3D();
     group.add(makeSegment(150,15))
     objects[id]={"element":group}
     return group;
    }


function makeSegment(lenght,thk)
    {
        var result=new THREE.Object3D();
        pShape=make_rect(lenght,50);
        sPath=make_rect_path(lenght,10);
        result.add(new THREE.Line(pShape.createPointsGeometry(),lineMaterial));
        var options = {
                        amount: thk,
                        steps: 1,
                        bevelSegments: 0,
                        bevelSize: 0,
                        bevelThickness: 0
                      };
        result.add(new THREE.Mesh(new THREE.ExtrudeGeometry(pShape, options),material));
        return result
    }


function update_shape()
    {
     if (objects.project){scene.remove(objects.project.element)}

     makeObject('project');
     scene.add(objects.project.element);
    }


$(".value").on("change",update_shape);
camera.position.set(0,-8000,0);
camera.up.set(0,0,1);
camera.updateProjectionMatrix ();
cameraControls.noRotate=true;
cameraControls.update();

