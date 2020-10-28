'''
'''
def script_str(uuid):
	mystr = """
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>
 <script >
    	//Round a float value to x.xx format
    	function roundWithTwoDecimals(value)
    	{{
    		var x = (Math.round(value * 100)) / 100;
			var y = x.toFixed(2);
			return y;
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
			var coord = $(transform).attr("translation").split(" ");
			var x = roundWithTwoDecimals(coord[0]);
			var y = roundWithTwoDecimals(coord[1]);
			var z = roundWithTwoDecimals(coord[2]);
			var position = 'x = ' + x + ' y = ' + y + ' z = ' + z;
    		$(''.concat('#position_', uuid)).html(position);
    	}}
        
        $(document).ready(function(){{
        	//Add a onMouseover callback to every shape
        	$("shape").each(function() {{
        		$(this).attr("onMouseover", "handleSingleClick_shape_{0}(this, this.id)");
        	}});
			//Add a onMouseover callback to every transform
        	$("transform").each(function() {{
        		$(this).attr("onMouseover", "handleSingleClick_transform_{0}(this, this.id)");
        	}});
        }});
		//Handle click on a transform
    	function ballstick_{0}(uuid = "{0}")
    	{{
    		var objs = document.getElementsByName(''.concat('at_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("scale", "0.6, 0.6, 0.6");
				}}
			bs_{0}(uuid = "{0}", "0")
			ps_{0}(uuid = "{0}", "-1")
        }}
		function spacefilling_{0}(uuid = "{0}")
    	{{
    		var objs = document.getElementsByName(''.concat('at_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("scale", "1.0, 1.0, 1.0");
				}}
			bs_{0}(uuid = "{0}", "-1")
			ps_{0}(uuid = "{0}", "-1")
        }}
		function polyhedra_{0}(uuid = "{0}")
    	{{
    		var objs = document.getElementsByName(''.concat('at_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("scale", "0.6, 0.6, 0.6");
				}}
			bs_{0}(uuid = "{0}", "0")
			ps_{0}(uuid = "{0}", "0")
        }}
		function none_{0}(uuid = "{0}")
    	{{
    		var objs = document.getElementsByName(''.concat('am_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("transparency", "0.0");
				}}
			ele_{0}(uuid = "{0}", "-1")
			ind_{0}(uuid = "{0}", "-1")
        }}
		
		function ele_{0}(uuid = "{0}", choice)
    	{{
		var objs = document.getElementsByName(''.concat('ele_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("whichChoice", choice);
				}}
        }}
		function ind_{0}(uuid = "{0}", choice)
    	{{
		var objs = document.getElementsByName(''.concat('ind_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("whichChoice", choice);
				}}
        }}
		function bs_{0}(uuid = "{0}", choice)
    	{{
		var objs = document.getElementsByName(''.concat('bs_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("whichChoice", choice);
				}}
        }}
		function ps_{0}(uuid = "{0}", choice)
    	{{
		var objs = document.getElementsByName(''.concat('ps_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("whichChoice", choice);
				}}
        }}
		function element_{0}(uuid = "{0}")
    	{{
    		var objs = document.getElementsByName(''.concat('am_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("transparency", "0.4");
				}}
			ele_{0}(uuid = "{0}", "0")
			bs_{0}(uuid = "{0}", "-1")
			ind_{0}(uuid = "{0}", "-1")
        }}
		function index_{0}(uuid = "{0}")
    	{{
    		var objs = document.getElementsByName(''.concat('am_', uuid));
			var max=objs.length;
			for (var i=0; i< max; i++) {{
				objs[i].setAttribute("transparency", "0.4");
				}}
			ind_{0}(uuid = "{0}", "0")
			bs_{0}(uuid = "{0}", "-1")
			ele_{0}(uuid = "{0}", "-1")
        }}
 </script> 
""".format(uuid)
	return mystr

def body_str(uuid):
	body_str = '''

<p>Models: 
<button type="button" onclick="ballstick_{0}()">  Ball-and-stick</button>
<button type="button" onclick="spacefilling_{0}()"> Space-filling</button>
<button type="button" onclick="polyhedra_{0}()"> Polyhedra</button>   
Labels: 
<button type="button" onclick="none_{0}()"> none</button>
<button type="button" onclick="element_{0}()"> element</button>
<button type="button" onclick="index_{0}()"> index</button>

<div id="camera_buttons" style="display: block;">
View:
    <button  onclick="document.getElementById('top_{0}').setAttribute('set_bind','true');">Top<br></button>
    <button  onclick="document.getElementById('front_{0}').setAttribute('set_bind','true');">Front<br></button>
    <button  onclick="document.getElementById('right_{0}').setAttribute('set_bind','true');">Right<br></button>
    <button onclick="document.getElementById('left_{0}').setAttribute('set_bind','true');">Left <br></button>
</div>

</p>
	<table style="font-size:1.0em;">
		<tr><td>Element: </td><td id="lastClickedObject_{0}">-</td> <td>  </td><td id="position_{0}">-</td></tr>
	</table>

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