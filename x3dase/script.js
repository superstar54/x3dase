//replace all uuid with real one.
let p1 = 'False';
let p2 = 'False';
let dist = '';
function set_viewpoint(uuid, view){
    $('#error_'.concat(atoms_dict['uuid'])).html('uuid: '.concat(atoms_dict["uuid"]));
    var persp = 'camera_persp_' + atoms_dict['uuid'];
    var ortho = 'camera_ortho_' + atoms_dict['uuid'];
    if (view == "top") {
        document.getElementById(persp).setAttribute('orientation','0 0 0 0');
        document.getElementById(persp).setAttribute('position', atoms_dict['top_pos']);
        document.getElementById(ortho).setAttribute('orientation','0 0 0 0');
        document.getElementById(ortho).setAttribute('position', atoms_dict['top_pos']);
    }
    else if (view == "front"){
        document.getElementById(persp).setAttribute('orientation','1 0 0 1.57079');
        document.getElementById(persp).setAttribute('position', atoms_dict['front_pos']);
        document.getElementById(ortho).setAttribute('orientation','1 0 0 1.57079');
        document.getElementById(ortho).setAttribute('position', atoms_dict['front_pos']);
        }
    else if (view == "right"){
        document.getElementById(persp).setAttribute('orientation','0 1 0 1.57079');
        document.getElementById(persp).setAttribute('position', atoms_dict['right_pos']);
        document.getElementById(ortho).setAttribute('orientation','0 1 0 1.57079');
        document.getElementById(ortho).setAttribute('position', atoms_dict['right_pos']);
    }
    else if (view == "left"){
        document.getElementById(persp).setAttribute('orientation','0 1 0 -1.57079');
        document.getElementById(persp).setAttribute('position', atoms_dict['left_pos']);
        document.getElementById(ortho).setAttribute('orientation','0 1 0 -1.57079');
        document.getElementById(ortho).setAttribute('position', atoms_dict['left_pos']);
    }
}

//Round a float value to x.xx format
function roundWithTwoDecimals(value)
{
    var x = (Math.round(value * 100)) / 100;
    var y = x.toFixed(2);
    return y;
}
        
//Add a onMouseover callback to every shape
$(document).ready(function(){
    $("shape").each(function() {
        $(this).attr("onMouseover", "handleOnMouseover_shape(this)");
        $(this).attr("onclick", "handleClick_shape(this)");
    });
    //Add a onMouseover callback to every transform
    $("transform").each(function() {
        $(this).attr("onMouseover", "handleOnMouseover_transform(this)");
        $(this).attr("onclick", "handleClick_transform(this)");
    });
});
//Handle onMouseover on a shape
function handleOnMouseover_shape(shape)
{
    var atom_kind = '#lastonMouseoverObject_kind_'.concat($(shape).attr("uuid"));
    var atom_index = '#lastonMouseoverObject_index_'.concat($(shape).attr("uuid"));
    $(atom_kind).html($(shape).attr("kind"));
    $(atom_index).html($(shape).attr("index"));
}
//Handle onMouseover on a transform
function handleOnMouseover_transform(transform)
{
    var atom_position = '#position_'.concat($(transform).attr("uuid"));
    var coord = $(transform).attr("translation").split(" ");
    var x = roundWithTwoDecimals(coord[0]);
    var y = roundWithTwoDecimals(coord[1]);
    var z = roundWithTwoDecimals(coord[2]);
    var position = 'x = ' + x + ' y = ' + y + ' z = ' + z;
    $(atom_position).html(position);
}
function handleClick_transform(transform)
{
    var distance = '#distance_'.concat($(transform).attr("uuid"));
    var id = $(transform).attr("id");
    if (p1 == 'False') { 
		p1 = id; 
        scale = document.getElementById(p1).getAttribute("translation");
    $('distance').html(dist);
		}
	else if(p2 == 'False') { 
		p2 = id; 
        calculate_distance(p1, p2);
        p1 = 'False';
        p2 = 'False';
        dist = '';
	}
}
function calculate_distance(p1, p2)
{
    var distance = '#distance_'.concat(document.getElementById(p1).getAttribute("uuid"));
    var c1 = document.getElementById(p1).getAttribute("translation").split(" ");
    var c2 = document.getElementById(p2).getAttribute("translation").split(" ");
    r = (c1[0] - c2[0])*(c1[0] - c2[0]) + (c1[1] - c2[1])*(c1[1] - c2[1]) + (c1[2] - c2[2])*(c1[2] - c2[2]);
    r = roundWithTwoDecimals(Math.sqrt(r));
    var dist = 'Distance:  ' + r;
    $(distance).html(dist);
    p1 = 'False';
    p2 = 'False';
}

//Handle models
function spacefilling(uuid)
{
    var objs = document.getElementsByName(''.concat('at_'.concat(uuid)));
    var max=objs.length;
    for (var i=0; i< max; i++) {
        objs[i].setAttribute("scale", "1.0, 1.0, 1.0");
        }
    document.getElementById('bs_'.concat(uuid)).setAttribute("whichChoice", '-1');
    document.getElementById('ps_'.concat(uuid)).setAttribute("whichChoice", '-1');
}
function ballstick(uuid)
{
    if (atoms_dict['bond']=='False'){ 
        alert('Please set bond parameter in your code, e.g. bond=1.0!');
    }
    var objs = document.getElementsByName(''.concat('at_'.concat(uuid)));
    var max=objs.length;
    for (var i=0; i< max; i++) {
        objs[i].setAttribute("scale", "0.6, 0.6, 0.6");
        }
    document.getElementById('bs_'.concat(uuid)).setAttribute("whichChoice", '0');
    document.getElementById('ps_'.concat(uuid)).setAttribute("whichChoice", '-1');
}
function polyhedra(uuid)
{
    if (atoms_dict['polyhedra']=='{}'){ 
        alert('Please set polyhedra parameter in your code, e.g. polyhedra={"Ti": ["O"]}!');
    }
    var objs = document.getElementsByName(''.concat('at_'.concat(uuid)));
    var max=objs.length;
    for (var i=0; i< max; i++) {
        objs[i].setAttribute("scale", "0.6, 0.6, 0.6");
        }
    document.getElementById('bs_'.concat(uuid)).setAttribute("whichChoice", '0');
    document.getElementById('ps_'.concat(uuid)).setAttribute("whichChoice", '0');
}
function none(uuid)
{
    var objs = document.getElementsByName(''.concat('am_'.concat(uuid)));
    var max=objs.length;
    for (var i=0; i< max; i++) {
        objs[i].setAttribute("transparency", "0.0");
        }
    document.getElementById('ele_'.concat(uuid)).setAttribute("whichChoice", '-1');
    document.getElementById('ind_'.concat(uuid)).setAttribute("whichChoice", '-1');
}
        
function element(uuid)
{
    if (atoms_dict['label']=='False'){ 
        $('#error_'.concat(uuid)).html('(^_^) To show element, please set label=True in your code!');
		return ;
	}
    var objs = document.getElementsByName(''.concat('am_'.concat(uuid)));
    var max=objs.length;
    for (var i=0; i< max; i++) {
        objs[i].setAttribute("transparency", "0.4");
        }
    document.getElementById('ele_'.concat(uuid)).setAttribute("whichChoice", '0');
    document.getElementById('ind_'.concat(uuid)).setAttribute("whichChoice", '-1');
    document.getElementById('bs_'.concat(uuid)).setAttribute("whichChoice", '-1');
}
function index(uuid)
{
    if (atoms_dict['label']=='False'){ 
        $('#error_'.concat(uuid)).html('(^_^) To show index, please set label=True in your code!');
		return ;
	}
    var objs = document.getElementsByName(''.concat('am_'.concat(uuid)));
    var max=objs.length;
    for (var i=0; i< max; i++) {
        objs[i].setAttribute("transparency", "0.4");
        }
    document.getElementById('ind_'.concat(uuid)).setAttribute("whichChoice", '0');
    document.getElementById('ele_'.concat(uuid)).setAttribute("whichChoice", '-1');
    document.getElementById('bs_'.concat(uuid)).setAttribute("whichChoice", '-1');
}