
function makeObject(id)
    {

     // get parameters
     var dia_max=parseFloat($("input[name='dia_max:number']").val());
     var dia_min=parseFloat($("input[name='dia_min:number']").val());
     var thickness=parseFloat($("input[name='thickness:number']").val());
     var height=parseFloat($("input[name='height:number']").val());
     var parts=parseFloat($("input[name='parts:number']").val());
     var delta_radius=(dia_max-dia_min)/2;


     /* crea lato obliquo tronco*/
     var d=(dia_max-dia_min)/2.0;
     var h=height;
     var s=thickness;

     var alfa=Math.atan(d/h)
     var h2=s*Math.sin(alfa)
     var h1=h-h2
     var beta=Math.atan(d/h1)
     h2=s*Math.sin(beta)
     var delta=h1+h2-h

     while (delta>0)
     {
      h1=h-h2;
      beta=Math.atan(d/h1);
      h2=s*Math.sin(beta);
      delta=h1+h2-h;
     }

     var d2=Math.pow(Math.pow(s,2)-Math.pow(h2,2),0.5);

     //
     var geom;
     var div;
     var vertices;
     var faces=[];
     var step;
     var alfa;

     var rad_max_ext=dia_max/2;
     var rad_min_ext=dia_min/2;

     var group = new THREE.Object3D();//create an empty container


     for (p=0 ; p<parts; p++)
     {
       div=180;
       vertices=[];
       faces=[];
       step=((Math.PI*2/parts)/div);
       start=p*(Math.PI*2/parts);
       geom=new THREE.Geometry();
       outlineGeo1 = new THREE.Geometry();
       outlineGeo2 = new THREE.Geometry();
       outlineGeo3 = new THREE.Geometry();
       outlineGeo4 = new THREE.Geometry();
       outlineGeo5 = new THREE.Geometry();
       outlineGeo6 = new THREE.Geometry();



       /* crea vertici superficie esterna */
       for (i = 0; i <=div; i++)
       {
         alfa=start+step*i;
         vertices.push(new THREE.Vector3(rad_max_ext*Math.cos(alfa),
                                         rad_max_ext*Math.sin(alfa),
                                         h2));
         vertices.push(new THREE.Vector3(rad_min_ext*Math.cos(alfa),
                                         rad_min_ext*Math.sin(alfa),
                                         height));
       }

       var rad_max_int=(dia_max/2)-d2;
       var rad_min_int=(dia_min/2)-d2;

       /* crea vertici superficie interna */
       for (i = 0; i <=div; i++)
       {
         alfa=start+step*i;
         vertices.push(new THREE.Vector3(rad_max_int*Math.cos(alfa),
                                         rad_max_int*Math.sin(alfa),
                                         0));
         vertices.push(new THREE.Vector3(rad_min_int*Math.cos(alfa),
                                         rad_min_int*Math.sin(alfa),
                                         h1));
       }



       /* crea facce superficie esterna */
       var countA=(div*2);
       for (i = 0; i <countA; i+=2)
       {
        faces.push( new THREE.Face3( i, i+2, i+1 ));
        faces.push( new THREE.Face3( i+2, i+3, i+1 ));
        outlineGeo1.vertices.push(vertices[i]);
        outlineGeo2.vertices.push(vertices[i+1]);
       }
       outlineGeo1.vertices.push(vertices[countA]);
       outlineGeo2.vertices.push(vertices[countA+1]);


       /* crea facce superficie interna */
       var countB=(div*4);
       for (i = countA+2; i <=countB; i+=2)
       {
        faces.push( new THREE.Face3( i, i+1, i+2 ) );
        faces.push( new THREE.Face3( i+2, i+1, i+3 ) );
        outlineGeo3.vertices.push(vertices[i]);
        outlineGeo4.vertices.push(vertices[i+1]);
       }
       outlineGeo3.vertices.push(vertices[countB+2]);
       outlineGeo4.vertices.push(vertices[countB+3]);
       outlineGeo5.vertices.push(vertices[0]);
       outlineGeo5.vertices.push(vertices[1]);
       outlineGeo5.vertices.push(vertices[countA+3]);
       outlineGeo5.vertices.push(vertices[countA+2]);
       outlineGeo5.vertices.push(vertices[0]);


       /* crea facce spessore inferiore */
       for (i = 0; i <countA; i+=2)
       {
        faces.push( new THREE.Face3( i, i+countA+2, i+2 ) );
        faces.push( new THREE.Face3( i+countA+2, i+countA+4, i+2 ) );
       }


       /* crea facce spessore inferiore */
       for (i = 1; i <countA+1; i+=2)
       {
        faces.push( new THREE.Face3( i, i+2, i+countA+2 ) );
        faces.push( new THREE.Face3( i+countA+2, i+2, i+countA+4 ) );
       }
       faces.push( new THREE.Face3( 0, 1, countA+2) );
       faces.push( new THREE.Face3( countA+2, 1, countA+3) );

       faces.push( new THREE.Face3( countA+1, countA, countB+3) );
       faces.push( new THREE.Face3( countB+2, countB+3, countA) );


       geom.vertices=vertices;
       geom.faces=faces;
       geom.computeFaceNormals();
       geom.mergeVertices();

       if (p==0)
       {
         material.transparent= false;
         material.opacity= 1.0;
         group.add( new THREE.Mesh( geom, material));//add a mesh with geometry to it
       }
       else
       {
         material2.transparent= true;
         material2.opacity= 0.2;
         group.add( new THREE.Mesh( geom, material2));//add a mesh with geometry to it
       }


       var line1 = new THREE.Line(outlineGeo1, lineMaterial);
       group.add(line1);
       var line2 = new THREE.Line(outlineGeo2, lineMaterial);
       group.add(line2);
       var line3 = new THREE.Line(outlineGeo3, lineMaterial);
       group.add(line3);
       var line4 = new THREE.Line(outlineGeo4, lineMaterial);
       group.add(line4);
       var line5 = new THREE.Line(outlineGeo5, lineMaterial);
       group.add(line5);
    }

    group.castShadow = group.receiveShadow = true;

    objects[id]={"element":group}


    return group;
    };




function update_shape()
    {


     if (objects.project){scene.remove(objects.project.element)}

     makeObject('project');
     scene.add(objects.project.element);

    }


$(".value").on("change",update_shape);

