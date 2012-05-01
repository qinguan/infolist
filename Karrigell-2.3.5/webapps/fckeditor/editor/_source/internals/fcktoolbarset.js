/*
 * FCKeditor - The text editor for internet
 * Copyright (C) 2003-2004 Frederico Caldeira Knabben
 * 
 * Licensed under the terms of the GNU Lesser General Public License:
 * 		http://www.opensource.org/licenses/lgpl-license.php
 * 
 * For further information visit:
 * 		http://www.fckeditor.net/
 * 
 * File Name: fcktoolbarset.js
 * 	Defines the FCKToolbarSet object that is used to load and draw the 
 * 	toolbar.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-05-31 23:07:50
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKToolbarSet = new Object() ;

FCKToolbarSet.Toolbars = new Array() ;

FCKToolbarSet.Expand = function()
{
	document.getElementById( 'Collapsed' ).style.display = 'none' ;
	document.getElementById( 'Expanded' ).style.display = '' ;
	
	if ( ! FCKBrowserInfo.IsIE )
	{
		// I had to use "setTimeout" because Gecko was not responding in a right
		// way when calling window.onresize() directly.
		window.setTimeout( "window.onresize()", 1 ) ;
	}
}

FCKToolbarSet.Collapse = function()
{
	document.getElementById( 'Collapsed' ).style.display = '' ;
	document.getElementById( 'Expanded' ).style.display = 'none' ;
	
	if ( ! FCKBrowserInfo.IsIE )
	{
		// I had to use "setTimeout" because Gecko was not responding in a right
		// way when calling window.onresize() directly.
		window.setTimeout( "window.onresize()", 1 ) ;
	}
}

FCKToolbarSet.Restart = function()
{
	if ( !FCKConfig.ToolbarCanCollapse || FCKConfig.ToolbarStartExpanded )
		this.Expand() ;
	else
		this.Collapse() ;
	
	document.getElementById( 'CollapseHandle' ).style.display = FCKConfig.ToolbarCanCollapse ? '' : 'none' ;
}

FCKToolbarSet.Load = function( toolbarSetName )
{
	this.DOMElement = document.getElementById( 'eToolbar' ) ;
	
	var ToolbarSet = FCKConfig.ToolbarSets[toolbarSetName] ;
	
	if (! ToolbarSet)
	{
		alert( 'Toolbar set "' + toolbarSetName + '" doesn\'t exist.' ) ;
		return ;
	}
	
	this.Toolbars = new Array() ;
	
	for ( var x = 0 ; x < ToolbarSet.length ; x++ ) 
	{
		var oToolbar = new FCKToolbar() ;
		
		for ( var j = 0 ; j < ToolbarSet[x].length ; j++ ) 
		{
			var sItem = ToolbarSet[x][j] ;
			
			if ( sItem == '-')
				oToolbar.AddSeparator() ;
			else
			{
				var oItem = FCKToolbarItems[sItem] ;
				if ( oItem )
					oToolbar.AddItem( oItem ) ;
				else
					alert( 'Unknown toolbar item name "' + sItem + "'" ) ;
			}
		}
		
		oToolbar.AddTerminator() ;
		
		this.Toolbars[ this.Toolbars.length ] = oToolbar ;
	}
	
	this.Redraw() ;
}

FCKToolbarSet.Redraw = function()
{
}

FCKToolbarSet.RefreshItemsState = function()
{
	
	for ( var i = 0 ; i < FCKToolbarSet.Toolbars.length ; i++ )
	{
		var oToolbar = FCKToolbarSet.Toolbars[i] ;
		for ( var j = 0 ; j < oToolbar.Items.length ; j++ )
		{
			oToolbar.Items[j].RefreshState() ;
		}
	}
}

