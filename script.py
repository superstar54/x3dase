from x3dase.tools import build_tag



script_str = '''
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>


 <script >
    	//Round a float value to x.xx format
    	function roundWithTwoDecimals(value)
    	{
    		return (Math.round(value * 100)) / 100;
    	}
    
    	//Handle click on any group member
    	function handleGroupClick(event)
    	{
    		//Mark hitting point
    		$('#marker').attr('translation', event.hitPnt);
    		console.log(event);
    		
    		//Display coordinates of hitting point (rounded)
    		var coordinates = event.hitPnt;
    		$('#coordX').html(roundWithTwoDecimals(coordinates[0]));
    		$('#coordY').html(roundWithTwoDecimals(coordinates[1]));
    		$('#coordZ').html(roundWithTwoDecimals(coordinates[2]));
    	}
    	
    	//Handle click on a shape
    	function handleSingleClick(shape)
    	{
    		$('#lastClickedObject').html($(shape).attr("def"));
    		
    	}
        
        $(document).ready(function(){
        	//Add a onclick callback to every shape
        	$("shape").each(function() {
        		$(this).attr("onclick", "handleSingleClick(this)");
        	});
        });

 </script> 
'''

body_str = '''
<div style="position:absolute;left:10px;top:10px;width:100px">
	<table style="font-size:1.0em;">
		<tr><td>Element: </td><td id="lastClickedObject">-</td></tr>
		<tr><td>X: </td><td id="coordX">-</td></tr>
		<tr><td>Y: </td><td id="coordY">-</td></tr>
		<tr><td>Z: </td><td id="coordZ">-</td></tr>
	</table>
</div>
'''

# script_str = build_tag('script', body = click)