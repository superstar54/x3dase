from x3dase.tools import build_tag


def script_str(uuid):
	mystr = """
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>
 <script >
    	//Round a float value to x.xx format
    	function roundWithTwoDecimals(value)
    	{{
    		return (Math.round(value * 100)) / 100;
    	}}
    	//Handle click on any group member
    	function handleGroupClick_{0}(event)
    	{{
    		//Mark hitting point
    		$('#marker').attr('translation', event.hitPnt);
    		console.log(event);
    		
    		//Display coordinates of hitting point (rounded)
    		var coordinates = event.hitPnt;
    		$('#pcoordX_{0}').html(roundWithTwoDecimals(coordinates[0]));
    		$('#pcoordY_{0}').html(roundWithTwoDecimals(coordinates[1]));
    		$('#pcoordZ_{0}').html(roundWithTwoDecimals(coordinates[2]));
    	}}
    	//Handle click on a shape
    	function handleSingleClick_shape_{0}(shape, uuid)
    	{{
    		$(''.concat('#lastClickedObject_', uuid)).html($(shape).attr("def"));
    	}}
		//Handle click on a transform
    	function handleSingleClick_transform_{0}(transform, uuid)
    	{{
    		$(''.concat('#coordX_', uuid)).html(roundWithTwoDecimals($(transform).attr("translation").split(" ")[0]));
    		$(''.concat('#coordY_', uuid)).html(roundWithTwoDecimals($(transform).attr("translation").split(" ")[1]));
    		$(''.concat('#coordZ_', uuid)).html(roundWithTwoDecimals($(transform).attr("translation").split(" ")[2]));
    	}}
        
        $(document).ready(function(){{
        	//Add a onclick callback to every shape
        	$("shape").each(function() {{
        		$(this).attr("onclick", "handleSingleClick_shape_{0}(this, this.id)");
        	}});
			//Add a onclick callback to every transform
        	$("transform").each(function() {{
        		$(this).attr("onclick", "handleSingleClick_transform_{0}(this, this.id)");
        	}});
        }});
 </script> 
""".format(uuid)
	return mystr

def body_str(uuid):
	body_str = '''
<div style="position:relative;left:10px;top:10px;width:100px">
	<table style="font-size:1.0em;">
		<tr><td>Element: </td><td id="lastClickedObject_{0}">-</td></tr>
		<tr><td>X: </td><td id="coordX_{0}">-</td></tr>
		<tr><td>Y: </td><td id="coordY_{0}">-</td></tr>
		<tr><td>Z: </td><td id="coordZ_{0}">-</td></tr>
	</table>
</div>
'''.format(uuid)
	return body_str



'''
function showx(obj)
	{{
		document.getElementById("x").innerHTML = $(obj).attr("translation").split(" ")[0];
		document.getElementById("y").innerHTML = $(obj).attr("translation").split(" ")[1];
		document.getElementById("z").innerHTML = $(obj).attr("translation").split(" ")[2];
	}}
'''