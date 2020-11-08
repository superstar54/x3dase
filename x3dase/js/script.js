
// if (atoms_dict[uuid]['new']){
function setQuality(uuid, quality){
        // $('#error_'.concat(atoms_dict[uuid]['uuid'])).html('uuid: '.concat(atoms_dict[uuid]["uuid"]));
        var x3d = 'x3dase_' + uuid;
        document.getElementById(x3d).setAttribute('PrimitiveQuality', quality);
    }
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
    var scale = target.parentNode.getAttribute('scale');
    scale = parseFloat(radius)*parseFloat(scale)*1.2;
    var scale = ' ' + scale + ' ' + scale + ' ' + scale;
    var translation = target.parentNode.getAttribute('translation');
    var id = target.parentNode.getAttribute('id');
    if (window.event.ctrlKey) {
        atoms_dict[uuid]['select'].push(id);

    }
    else {
        for (var i=1; i<= atoms_dict[uuid]['select'].length; i++) {
            $('#switch_marker_' + i + '_' + uuid).attr('whichChoice', -1);
        }
        atoms_dict[uuid]['select'] = [];
        atoms_dict[uuid]['select'].push(id);
        $('#switch_marker_' + 2 + '_' + uuid).attr('whichChoice', -1);
}
    var n = atoms_dict[uuid]['select'].length;
    $('#switch_marker_' + n + '_' + uuid).attr('whichChoice', 0);
    $('#marker_' + n + '_' + uuid).attr('translation', translation);
    $('#marker_' + n + '_' + uuid).attr('scale', scale);
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

    if (atoms_dict[uuid]['select'].length == 2){
        calculate_distance(uuid);
        draw_line(uuid);
    }
    else if (atoms_dict[uuid]['select'].length == 3){
        calculate_angle(uuid);
        draw_line(uuid);
    }

    console.log(event);
}
//Add a onMouseover callback to every shape
$(document).ready(function(){
    $("shape").each(function() {
        // $(this).attr("onMouseover", "handleOnMouseover_shape(this)");
        // $(this).attr("onclick", "handleClick_shape(this)");
    });
    //Add a onMouseover callback to every transform
    $("transform").each(function() {
        // $(this).attr("onMouseover", "handleOnMouseover_transform(this)");
        // $(this).attr("onclick", "handleClick_transform(this)");
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

function calculate_distance(uuid)
{
    var measure = '#measure_'.concat(uuid);
    var c1 = document.getElementById(atoms_dict[uuid]['select'][0]).getAttribute("translation").split(" ");
    var c2 = document.getElementById(atoms_dict[uuid]['select'][1]).getAttribute("translation").split(" ");
    r = (c1[0] - c2[0])*(c1[0] - c2[0]) + (c1[1] - c2[1])*(c1[1] - c2[1]) + (c1[2] - c2[2])*(c1[2] - c2[2]);
    r = roundWithTwoDecimals(Math.sqrt(r));
    var dist = 'Distance:  ' + r;
    $(measure).html(dist);
}
function calculate_angle(uuid)
{
    var measure = '#measure_'.concat(uuid);
    var c1 = document.getElementById(atoms_dict[uuid]['select'][0]).getAttribute("translation").split(" ");
    var c2 = document.getElementById(atoms_dict[uuid]['select'][1]).getAttribute("translation").split(" ");
    var c3 = document.getElementById(atoms_dict[uuid]['select'][2]).getAttribute("translation").split(" ");
    var AB = Math.sqrt(Math.pow(c2[0]-c1[0],2)+ Math.pow(c2[1]-c1[1],2) + Math.pow(c2[2]-c1[2],2));    
    var BC = Math.sqrt(Math.pow(c2[0]-c3[0],2)+ Math.pow(c2[1]-c3[1],2) + Math.pow(c2[2]-c3[2],2)); 
    var AC = Math.sqrt(Math.pow(c3[0]-c1[0],2)+ Math.pow(c3[1]-c1[1],2)+ Math.pow(c3[2]-c1[2],2));
    var angle = roundWithTwoDecimals(Math.acos((BC*BC+AB*AB-AC*AC)/(2*BC*AB))*180/3.1415926);
    var angle = 'angle:  ' + angle;
    $(measure).html(angle);
}
function draw_line(uuid)
{
    var n = atoms_dict[uuid]['select'].length;
    var coordIndex = '';
    var point = document.getElementById(atoms_dict[uuid]['select'][0]).getAttribute("translation");
    for (var i = 1; i < n; i++) {
        var c1 = document.getElementById(atoms_dict[uuid]['select'][i]).getAttribute("translation");
        coordIndex = coordIndex + (i-1) + ' ' + i + ' -1 ';
        point = point + ' ' + c1 + ' ';
    }
    $('#line_coor_' + 0 + '_' + uuid).attr('point', point);
    $('#line_ind_' + 0 + '_' + uuid).attr('coordIndex', coordIndex);
    $('#switch_line_' + 0 + '_' + uuid).attr('whichChoice', 0);
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
    if (atoms_dict[uuid]['bond']=='False'){ 
        alert('Please set bond parameter in your code, e.g. bond=1.0!');
        $('#error_'.concat(uuid)).html('(^_^) Please set bond parameter in your code, e.g. bond=1.0!');
		return ;
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
    if (atoms_dict[uuid]['polyhedra'].length==0){ 
        alert('Please set polyhedra parameter in your code, e.g. polyhedra={"Ti": ["O"]}!');
        $('#error_'.concat(uuid)).html('(^_^) Please set polyhedra parameter in your code, e.g. polyhedra={"Ti": ["O"]}!');
		return ;
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
    if (atoms_dict[uuid]['label']=='False'){ 
        alert('To show element, please set label=True in your code!');
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
    if (atoms_dict[uuid]['label']=='False'){ 
        alert('To show index, please set label=True in your code!');
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
// }