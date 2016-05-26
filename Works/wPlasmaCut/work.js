//var items=[];
var items={
            active:null,
            countId:1,
            list:{}
          }

var positions=[];
var obj3D;
var matSelected = new THREE.MeshLambertMaterial({color: 0x027002});

function loaditems(n)
{
    var f = n.target.files[0];

    if (f)
    {
        var r = new FileReader();
        r.onload = function(e)
                   {
                        var contents = e.target.result;
                        var item=JSON.parse(contents)
                        var workFlow=item.WorkFlow[0];
                        //alert (JSON.stringify(workFlow));
                        var trcontent='<tr id="'+items.countId+'">';
                        trcontent+= '<td>'+(items.countId)+'</td>';
                        trcontent+= '<td>'+f.name.split(".")[0]+'</td>';
                        trcontent+= '<td><input class="number" name="richiesti" value=1 type="number"'
                        trcontent+= ' style="width:90%"</input></td>';
                        trcontent+= '<td>0</td>';
                        trcontent+='</tr>';
                        $('tr#listitems tr:last').after(trcontent);
                        //items.push(workFlow);
                        items.list[items.countId]=workFlow;
                        items.countId+=1;
                    }
        r.readAsText(f);
    }
    else {alert("Failed to load file");}
};


function clearall(){alert ('cancello!!!!')};


var sheetshape


function makeSheet()
{
    if (sheetshape){scene.remove(sheetshape);}
    var width=parseFloat($("input[name='swidth:number']").val());
    var height=parseFloat($("input[name='altezza:number']").val());
    var thickness=1;
    //var shapePath=make_rect(width,height)
    var shapePath=meTHREE.makeRect(0,0,width,height)
    var options = {amount: thickness,
                   steps: 1,
                   bevelSegments: 0,
                   bevelSize: 0,
                   bevelThickness: 0
                  };


    wWidth = parseFloat($('#3Dscene').css('width'));
    wHeight = parseFloat($('#3Dscene').css('height'));
    viewSize=width;
    aspectRatio=wWidth/wHeight;
    var xViewOffset=-width/4;
    camera.left=(-aspectRatio*viewSize /2)+width/2+xViewOffset;
    camera.right=(aspectRatio* viewSize / 2)+width/2+xViewOffset;
    camera.top= viewSize / 2+height/2;
    camera.bottom=-viewSize / 2+height/2;
    camera.position.z= 8000;
    camera.position.y= 0;
    camera.position.x= 0;
    camera.updateProjectionMatrix ();
    cameraControls= new THREE.OrthographicTrackballControls(camera,renderer.domElement);
    cameraControls.noRotate=true;


    sheetshape= new THREE.Mesh( new THREE.ExtrudeGeometry(shapePath, options),material);
    sheetshape.castShadow = sheetshape.receiveShadow = true;
    scene.add(sheetshape);
}


function update_scene()
{
    makeSheet();
    for (i in items.list)
    {
    var shape=drawShape(items.list[id].Chain,items.list[id].Nodes,items.list[id].BoundBox)
    // add it to the scene.
    var options = {amount: 10,
                    steps: 1,
                    bevelSegments: 0,
                    bevelSize: 0,
                    bevelThickness: 0
                   };


    var obj3D= new THREE.Mesh( new THREE.ExtrudeGeometry(shape, options),material2);
    obj3D.castShadow = obj3D.receiveShadow = true;
    sheetshape.add(obj3D);
    }

}


function insertItem()
{
    //crea elenco items
    var id=positions.length;
    //var opt='<option value="-1"></option>';
    var opt='';
    for (i in items.list)
    {
        opt+='<option value="'+i+'">'+$("table#listitems tr#"+i+" td:eq(1)").text()+'</option>';
    }
    //cambia funzione pulsante
    var content='<a onclick="confirmItem('+id+')" id="positions_button_confirm"'+
                ' class="button" data-w2p_disable_with="default">Conferma</a><span> </span>'
    $('#positions_button_insert').replaceWith(content);
    var trcontent='<tr>';
    trcontent+= '<td><a>1</a></td>';
    trcontent+= '<td><select id='+id+'>'+opt+'</select></td>';
    trcontent+= '<td name="x">1500</td>';
    trcontent+= '<td name="y">750</td>';
    trcontent+= '<td name="degree">0</td>';
    trcontent+= '</tr>';
    $('tr#positions tr:last').after(trcontent);
}


function confirmItem(num)
{
    console.log('num:',num);
    var id;
    positions.push({"articolo_id":2,"x":2,"y":3,"gradi":5});
    var content='<a onclick="insertItem()" id="positions_button_insert"'+
                ' class="button" data-w2p_disable_with="default">Inserisci</a>'
    $('#positions_button_confirm').replaceWith(content);
    id=parseInt($("select[id="+num+"]").val());
    console.log('id:',id);



    //var shape=drawShape(items[id].Chain,items[id].Nodes,items[id].BoundBox);
    var shape=drawShape(items.list[id].Chain,items.list[id].Nodes,items.list[id].BoundBox)
    // add it to the scene.
    var options = {amount: 10,
                    steps: 1,
                    bevelSegments: 0,
                    bevelSize: 0,
                    bevelThickness: 0
                   };


    var obj3D= new THREE.Mesh( new THREE.ExtrudeGeometry(shape, options),material2);
    obj3D.castShadow = obj3D.receiveShadow = true;
    sheetshape.add(obj3D);
}



function deleteItem()
{
    alert ('deletItem')
}



function getMousePos(evt) {
        var rect =document.getElementById("3Dscene").getBoundingClientRect();
        return {
          x: evt.clientX - rect.left,
          y: evt.clientY - rect.top
        };
      }


function onDocumentMouseMove( event )
{
    var scenemousepos=getMousePos(event);
    mouse.x = ( scenemousepos.x /  wWidth ) * 2 - 1;
	mouse.y = - ( scenemousepos.y /  wHeight ) * 2 + 1;

    raycaster.setFromCamera( mouse, camera );
    intersection = raycaster.intersectObjects(scene.children);
    if (intersection.length!=0)
    {
     console.log(intersection[0].object.uuid);
     $('#X').text('X:'+intersection[0].point.x.toFixed(2))
     $('#Y').text('Y:'+intersection[0].point.y.toFixed(2))
    }
    else
     {
     $('#X').text('X:')
     $('#Y').text('Y:')
    }
    //console.log(selected);
    if (selection.active)
    {
      if (rotate)
      {
        var p2={X:intersection[0].point.x,Y:intersection[0].point.y};
        var p1={X:selection.object.position.x,Y:selection.object.position.y};
        var a=PointsVector(p1,p2)[1];
        var delta=a-selection.actualDegree

        var newAngle=selection.object.rotation.z+delta
        if (newAngle>2*Math.PI){newAngle=newAngle-2*Math.PI}
        if (newAngle<0){newAngle=newAngle+2*Math.PI}
        console.log('new angle:',newAngle);

        var delta=0.05

        if (Math.abs(newAngle-Math.PI)<delta)
        {
            console.log('kept in 180° rotation')
            newAngle=Math.PI;
        }
        else if (Math.abs(newAngle)<delta || Math.abs(newAngle-2*Math.PI)<delta )
        {
            console.log('kept in 0° rotation')
            newAngle=0;
        }
        else if (Math.abs(newAngle-Math.PI/2)<delta)
        {
            console.log('kept in 90° rotation')
            newAngle=Math.PI/2;
        }
        else if (Math.abs(newAngle-3*Math.PI/2)<delta)
        {
            console.log('kept in 270° rotation')
            newAngle=3*Math.PI/2;
        }
        else{selection.actualDegree=a}

        selection.object.rotation.z = newAngle;

      }
      else
      {
        selection.object.position.x += intersection[0].point.x-selection.actualPos.x;
        selection.object.position.y += intersection[0].point.y-selection.actualPos.y;
        selection.actualPos=intersection[0].point;
      }
    }
}


function onDocumentMouseDown (event)
{
  event.preventDefault();
  mousedown=true;
  console.log(event.button);
  raycaster.setFromCamera( mouse, camera );
  raySelect = raycaster.intersectObjects(sheetshape.children);
  if (raySelect.length!=0)
  {
      selection.active=true;
      selection.object=raySelect[0].object;
      //console.log(selection.object);
      selection.material=selection.object.material
      selection.object.material=matSelected;
      selection.actualPos=raySelect[0].point;
  }
  else
  {
      selection.active=false;
      selection.object=null;
  }
}

function onDocumentMouseUp (event)
{

  mousedown=false;
  if (selection.active){selection.object.material=selection.material;}
  selection.active=false;
  selection.object=null;

}

function onKeyDown (event)
{
  if (event.keyCode==226 && selection.active)
  {
      rotate=true
      var p2={X:intersection[0].point.x,Y:intersection[0].point.y};
      var p1={X:selection.object.position.x,Y:selection.object.position.y};
      selection.actualDegree=PointsVector(p1,p2)[1];
  }
  else{rotate=false}
  //console.log('rotate:',rotate);
}


function onKeyUp (event)
{
  if (event.keyCode==226)
  {
      rotate=false
      selection.actualPos=intersection[0].point;
  }
  //console.log('rotate:',rotate);
}



var intersection,raySelect
var selection={
                active:false,
                object:null,
                actualPos:new THREE.Vector2(),
                actualDegree:null,
                material:null
              };
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
var mousedown=false;
var rotate=false;
document.addEventListener('mousemove', onDocumentMouseMove, false );
renderer.domElement.addEventListener( 'mousedown', onDocumentMouseDown, false );
renderer.domElement.addEventListener( 'mouseup', onDocumentMouseUp, false );
document.addEventListener( 'keydown', onKeyDown, false );
document.addEventListener( 'keyup', onKeyUp, false );
