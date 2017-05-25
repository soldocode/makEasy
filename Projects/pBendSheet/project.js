
function makeObject(id)
    {
     var thk=1
     var group = new THREE.Object3D();
     var segment = new THREE.Object3D();
     pShape=make_rect(100,50);
     sPath=make_rect_path(100,50);
     segment.add(new THREE.Line(pShape.createPointsGeometry(),lineMaterial));
     var options = {
                        amount: thk,
                        steps: 1,
                        bevelSegments: 0,
                        bevelSize: 0,
                        bevelThickness: 0
                      };
     segment.add(new THREE.Mesh(new THREE.ExtrudeGeometry(pShape, options),material));
     segment.castShadow = group.receiveShadow = true;
     objects[id]={"element":segment}
     return segment;
    }

function update_shape()
    {
     if (objects.project){scene.remove(objects.project.element)}

     makeObject('project');
     scene.add(objects.project.element);
    }


$(".value").on("change",update_shape);