
  
    $(".value").on("change",update_shape);

    
    function makePlate(p)
    {
        alert('olà Plate');
    }

    function makeObject()
    {
     var type_shape= $("select[name='shape:number']").val();

     if (type_shape==1)
     {
      length=$("input[name='misure2:number']").val();
      height=$("input[name='misure3:number']").val();
      rectShape=make_rect(length,height);
      shapePath=make_rect_path(length,height);
     }
     else
     {
      length=$("input[name='misure4:number']").val();
      rectShape=make_circle(length);
      shapePath=make_circle_path(length);
     }


     var id_hole=$("input[name='id_holes']").val()
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
        var num_holes=$("input[name='holes["+i+"][num]:number']").val();
        var dstart=$("input[name='holes["+i+"][par]:number']").val();
        var int_holes=$("input[name='holes["+i+"][intfo]:number']").val();
        for (var c = 1; c <= num_holes; c++)
        {
         theta = (((Math.PI * 2)/ num_holes)*c)+((dstart)/360*(Math.PI * 2));
         px= Math.cos(theta) * (int_holes/2);
         py= Math.sin(theta) * (int_holes/2);
         //rectShape.holes.push(make_hole($("input[name='holes["+i+"][dia]:number']").val(),px,py));
         shapeHolePath=make_hole_path($("input[name='holes["+i+"][dia]:number']").val(),px,py);
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
        rectShape.holes.push(hpath);
      }


     var options = {amount: $("input[name='misure1:number']").val(),
                    steps: 1,
                    bevelSegments: 0,
                    bevelSize: 0,
                    bevelThickness: 0
                   };

     return new THREE.Mesh( new THREE.ExtrudeGeometry(rectShape, options),material);
    }




    function update_shape()
    {
     wWidth = parseFloat($('#3Dscene').css("width"));
     wHeight = parseFloat($('#3Dscene').css('height'));
     aspectRatio=wWidth/wHeight;
     viewSize=$("input[name='misure2:number']").val();
     camera.left = -aspectRatio*viewSize/1.5 ;
     camera.right = aspectRatio* viewSize /1.5;
     camera.top = viewSize /1.5;
     camera.bottom = - viewSize/1.5 ;
     camera.updateProjectionMatrix();

     scene.remove(extshape);
     extshape=makeObject();


     // add it to the scene.
     extshape.castShadow = extshape.receiveShadow = true;
     scene.add(extshape);

    }

ITEMS3D['pPlate']=makePlate;
