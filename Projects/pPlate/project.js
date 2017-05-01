

    meProject.makePlate= function(pp)
    {
       var plate= new THREE.Object3D();
       var type_shape= pp.shape;
       var thk=pp.misure1;

       if (type_shape==1)
        {
         length=pp.misure2;
         height=pp.misure3;
         pShape=make_rect(length,height);
         sPath=make_rect_path(length,height);
         }
        else
        {
         length=pp.misure4;
         pShape=make_circle(length);
         sPath=make_circle_path(length);
        }

        plate.add(new THREE.Line(pShape.createPointsGeometry(),lineMaterial));
        var thkLine=new THREE.Line(pShape.createPointsGeometry(),lineMaterial);
        thkLine.position.z=thk;
        plate.add(thkLine);

        var id_hole=pp.id_holes;
        var shapeHolesPaths=[];
        var cpr = new ClipperLib.Clipper();
        var solution_paths = [];
        var scale = 100;
        var shapeHolePath;
        var theta,px,py;
        if (id_hole>-1)
        {
            for (var i = 0; i <= id_hole; i++)
            {
                var num_holes=pp.holes[i].num;
                var dstart=pp.holes[i].par;
                var int_holes=pp.holes[i].intfo;
                for (var c = 1; c <= num_holes; c++)
                {
                    theta = (((Math.PI * 2)/ num_holes)*c)+((dstart)/360*(Math.PI * 2));
                    px= Math.cos(theta) * (int_holes/2);
                    py= Math.sin(theta) * (int_holes/2);
                    shapeHolePath=make_hole_path(pp.holes[i].dia,px,py);
                    ClipperLib.JS.ScaleUpPaths(shapeHolePath, scale);
                    cpr.AddPath(shapeHolePath, ClipperLib.PolyType.ptSubject, true);
                    cpr.AddPaths(solution_paths, ClipperLib.PolyType.ptClipt, true);
                    var succeeded = cpr.Execute(1, solution_paths, 1, 1);
                }
            }
        }

        for (var h in solution_paths)
        {
            var curpath=solution_paths[h];
            var hpath = new THREE.Path();
            hpath.moveTo(curpath[0].X,curpath[0].Y);
            for (var i = 1; i <curpath.length; i++)
            {
                hpath.lineTo(curpath[i].X,curpath[i].Y);
            }
            hpath.lineTo(curpath[0].X,curpath[0].Y);
            pShape.holes.push(hpath);
            plate.add(new THREE.Line(hpath.createPointsGeometry(),lineMaterial));
            var thkLine=new THREE.Line(hpath.createPointsGeometry(),lineMaterial);
            thkLine.position.z=thk;
            plate.add(thkLine);
        }

        var options = {
                        amount: thk,
                        steps: 1,
                        bevelSegments: 0,
                        bevelSize: 0,
                        bevelThickness: 0
                      };

        plate.add(new THREE.Mesh( new THREE.ExtrudeGeometry(pShape, options),material));
        plate.castShadow = plate.receiveShadow = true;

       return plate
    }


    function getParameters()
    {
        var p={}
        p.shape=$("select[name='shape:number']").val();
        p.misure1=$("input[name='misure1:number']").val();
        p.misure2=$("input[name='misure2:number']").val();
        p.misure3=$("input[name='misure3:number']").val();
        p.misure4=$("input[name='misure4:number']").val();
        p.id_holes=$("input[name='id_holes']").val();
        p.holes=[];
        if (p.id_holes >-1)
        {
         for (var i = 0; i <= p.id_holes; i++)
           {
             var h={}
             h.num=$("input[name='holes["+i+"][num]:number']").val();
             h.par=$("input[name='holes["+i+"][par]:number']").val();
             h.intfo=$("input[name='holes["+i+"][intfo]:number']").val();
             h.dia=$("input[name='holes["+i+"][dia]:number']").val();
             p.holes.push(h);
           }
        }
        return p
    }



    function makeObject(id)
    {
        objects[id]={"element":meProject.makePlate(getParameters())}
        return objects[id].element

    }



    function update_shape()
    {

     if (objects.project)
     {
         scene.remove(objects.project.element);
     }

     makeObject('project');
     scene.add(objects.project.element);

    }

    $(".value").on("change",update_shape);
