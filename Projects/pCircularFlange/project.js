
meProject.makeCircularFlange= function(pp)
{
    var obj= new THREE.Object3D();
    var thk=parseFloat(pp.sheet_thk);


    length=pp.dia_est;
    pShape=make_circle(length);
    sPath=make_circle_path(length);

    // diameter external
    obj.add(new THREE.Line(pShape.createPointsGeometry(),lineMaterial));
    var thkLine=new THREE.Line(pShape.createPointsGeometry(),lineMaterial);
    thkLine.position.z=thk;
    obj.add(thkLine);

    // diameter internal
    if (pp.dia_int>0 && pp.dia_int<pp.dia_est)
    {
        var hole_shape=make_hole(pp.dia_int,0,0);
        pShape.holes.push(hole_shape);
        obj.add(new THREE.Line(hole_shape.createPointsGeometry(),lineMaterial));
        var thkLine=new THREE.Line(hole_shape.createPointsGeometry(),lineMaterial);
        thkLine.position.z=thk;
        obj.add(thkLine)
    }

    // holes
    var id_hole=pp.id_holes;
    var theta,px,py;
    if (id_hole>-1)
        {
            for (var i = 0; i <= id_hole; i++)
            {
                var num_holes=pp.holes[i].num;
                console.log(num_holes);
                var dstart=pp.holes[i].par;
                var int_holes=pp.holes[i].intfo;
                var chd=pp.holes[i].circular_holes_dia
                for (var c = 1; c <= num_holes; c++)
                {
                    theta = (((Math.PI * 2)/ num_holes)*c)+((dstart)/360*(Math.PI * 2));
                    px= Math.cos(theta) * (int_holes/2);
                    py= Math.sin(theta) * (int_holes/2);
                    var curpath=make_hole_path(chd,px,py);

                    var hpath = new THREE.Path();
                    hpath.moveTo(curpath[0].X,curpath[0].Y);
                    for (var n = 1; n <curpath.length; n++)
                    {
                        hpath.lineTo(curpath[n].X,curpath[n].Y);
                    }
                    hpath.lineTo(curpath[0].X,curpath[0].Y);
                    pShape.holes.push(hpath);
                    obj.add(new THREE.Line(hpath.createPointsGeometry(),lineMaterial));
                    var thkLine=new THREE.Line(hpath.createPointsGeometry(),lineMaterial);
                    thkLine.position.z=thk;
                    obj.add(thkLine);
                }
           }
        }

    var options = {
                    amount: thk,
                    steps: 1,
                    bevelSegments: 0,
                    bevelSize: 0,
                    bevelThickness: 0
                  };

    obj.add(new THREE.Mesh( new THREE.ExtrudeGeometry(pShape, options),material));
    obj.castShadow = obj.receiveShadow = true;

    return obj
}



function makeObject(id)
{
    objects[id]={"element":meProject.makeCircularFlange(JSON.parse(localStorage.prj_data))}
    return objects[id].element
}


function update_shape()
{
    if (objects.project){scene.remove(objects.project.element);}
    makeObject('project');
    scene.add(objects.project.element);
}


function addHolesForm()
{
    dia_est=parseFloat($("input[name='dia_est:number']").val())
    dia_int=parseFloat($("input[name='dia_int:number']").val())
    dia_middle=(dia_est+dia_int)/2
    count=$("input[name='id_holes']").val()
    form=[{"name":"circular_holes","class":"hole","value":"{\"type\":\"1\",\"dia\":\"20\"}"},
          {"name":"intfo","args":{},"value":dia_middle,"label":"interasse foratura","width":40,"class":"number"},
          {"name":"num","args":{},"value":1,"label":"numero fori","width":40,"class":"number"},
          {"name":"par","args":{},"value":0,"label":"angolo primo foro","width":40,"class":"number"}]
    meForm.addSForm({"count":count,
                     "form":form,
                     "class":"multiple-subform",
                     "after_deletion_callback":"refresh_form",
                     "add_button":{"args":{},"label":"Aggiungi Foratura"},
                     "label":"foratura",
                     "id":"holes"})
}


function after_deploy()
{
    meForm.SheetMaterial.updateMaterialField('sheet');
}

meForm.afterDeployForm=after_deploy
$(".value").on("change",update_shape);
