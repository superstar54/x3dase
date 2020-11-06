
//replace all uuid with real one.
if (atoms_dict['new']){
function set_viewpoint(uuid, pos, ori){
    // $('#error_'.concat(atoms_dict[uuid]['uuid'])).html('uuid: '.concat(atoms_dict[uuid]["uuid"]));
    var persp = 'camera_persp_' + uuid;
    var ortho = 'camera_ortho_' + uuid;
    document.getElementById(persp).setAttribute('orientation', atoms_dict[uuid][ori]);
    document.getElementById(persp).setAttribute('position', atoms_dict[uuid][pos]);
    document.getElementById(ortho).setAttribute('orientation', atoms_dict[uuid][ori]);
    document.getElementById(ortho).setAttribute('position', atoms_dict[uuid][pos]);
}

//Round a float value to x.xx format
function roundWithTwoDecimals(value)
{
    var x = (Math.round(value * 100)) / 100;
    var y = x.toFixed(2);
    return y;
}
//Handle click on any group member
function handleGroupClick(event)
{
    //Mark hitting point
    var target = event.target;
    var uuid = target.parentNode.getAttribute('uuid')
    var radius = target.parentNode.getAttribute('radius');
    radius = (Math.round(radius * 100)) / 100*1.1;
    var scale = ' ' + radius + ' ' + radius + ' ' + radius;
    var translation = target.parentNode.getAttribute('translation');
    $('#switch_marker_'.concat(uuid)).attr('whichChoice', 0);
    $('#marker_'.concat(uuid)).attr('translation', translation);
    $('#marker_'.concat(uuid)).attr('scale', scale);

    var atom_kind = '#lastonMouseoverObject_kind_'.concat(uuid);
    var atom_index = '#lastonMouseoverObject_index_'.concat(uuid);
    $(atom_kind).html(target.getAttribute("kind"));
    $(atom_index).html(target.getAttribute("index"));
    //
    var coord = translation.split(" ")
    var atom_position = '#position_'.concat(uuid);
    var x = roundWithTwoDecimals(coord[0]);
    var y = roundWithTwoDecimals(coord[1]);
    var z = roundWithTwoDecimals(coord[2]);
    var position = 'x = ' + x + ' y = ' + y + ' z = ' + z;
    $(atom_position).html(position);
    console.log(event);
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
$(document).on("click", function(e) {
    if (e.target === document || e.target.tagName === "BODY" || e.target.tagName === "HTML") {
        $('#marker').attr('scale', "0.0001 0.0001 0.0001");
    }
});
//Handle onMouseover on a shape
function handleOnMouseover_shape(shape)
{
    var atom_kind = '#lastonMouseoverObject_kind_'.concat($(shape).attr("uuid"));
    var atom_index = '#lastonMouseoverObject_index_'.concat($(shape).attr("uuid"));
    $(atom_kind).html($(shape).attr("kind"));
    $(atom_index).html($(shape).attr("index"));
}
//Handle onMouseover on a shape
function handleClick_shape(shape)
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
    var coord = $(transform).attr("translation").split(" "[0]);
    var x = roundWithTwoDecimals(coord[0]);
    var y = roundWithTwoDecimals(coord[1]);
    var z = roundWithTwoDecimals(coord[2]);
    var position = 'x = ' + x + ' y = ' + y + ' z = ' + z;
    $(atom_position).html(position);
}
function handleClick_transform(transform)
{
    var uuid = $(transform).attr("uuid");
    var distance = '#distance_'.concat(uuid);
    var id = $(transform).attr("id");
    if (atoms_dict[uuid]['p1'] == 'false') { 
		atoms_dict[uuid]['p1'] = id; 
    // $('distance').html('p1');
		}
	else if(atoms_dict[uuid]['p2'] == 'false') { 
		atoms_dict[uuid]['p2'] = id; 
        calculate_distance(uuid, atoms_dict[uuid]['p1'], atoms_dict[uuid]['p2']);
        atoms_dict[uuid]['p1'] = 'false';
        atoms_dict[uuid]['p2'] = 'false';
	}
}
function calculate_distance(uuid, p1, p2)
{
    var distance = '#distance_'.concat(uuid);
    var c1 = document.getElementById(p1).getAttribute("translation").split(" ");
    var c2 = document.getElementById(p2).getAttribute("translation").split(" ");
    r = (c1[0] - c2[0])*(c1[0] - c2[0]) + (c1[1] - c2[1])*(c1[1] - c2[1]) + (c1[2] - c2[2])*(c1[2] - c2[2]);
    r = roundWithTwoDecimals(Math.sqrt(r));
    var dist = 'Distance:  ' + r;
    $(distance).html(dist);
    atoms_dict[uuid]['p1'] = 'false';
    atoms_dict[uuid]['p2'] = 'false';
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
    if (atoms_dict['bond']=='false'){ 
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
    if (atoms_dict['label']=='false'){ 
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
    if (atoms_dict['label']=='false'){ 
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
}