
var Utils = function() {

	this.format_date = function(dt) {

		var utils = new Utils();
		return utils.format_datetime(dt).split(' ')[0];
	};

	this.format_datetime = function(dt) {

		var year = dt.split(' ')[0].split('-')[0];
		var month = dt.split(' ')[0].split('-')[1];
		var day = dt.split(' ')[0].split('-')[2];

		var hour = dt.split(' ')[1].split(':')[0];
		var minute = dt.split(' ')[1].split(':')[1];
		var second = dt.split(' ')[1].split(':')[2].split('.')[0];		

		return '' + month + '/' + day + '/' + year + ' ' + hour + ':' + minute + ':' + second;
	};

	this.build_token_param = function() {
		var token_param = '';
		var utils = new Utils();
		if ( utils.get_params().token ) {
			token_param = 'token=' + utils.get_params().token;
		}
		return token_param;
	};

	// validate a callback can be called
	this.valid_callback = function(callback) {
		var valid = false;
		if( callback != null && callback != undefined && typeof(callback) != 'undefined') {
			valid = true;
		}
		return valid;
	};

	// replaces keys with vals in html text
	//   notes: supports {{key}} and ##key##
	this.populate_page_html = function(html, vars) {
		for(var key in vars) {
			var re0 = new RegExp('{{' + key + '}}', 'g');
			var re1 = new RegExp('##' + key + '##', 'g');
			html = html.replace(re0, vars[key]);
			html = html.replace(re1, vars[key]);
		}
		return html;
	},

	// handle hash change for new browsers and old
	this.change_hash = function(new_hash) {
		console.log('Utils.change_hash(), new_hash = ', new_hash);
		//if(history.pushState) {
		//    history.pushState(null, null, new_hash);
		//}
		//else {
			console.log ( location )
			//if ( window.location.split('/')
		    location.hash = new_hash;
		//}
	};

	this.redirect = function(new_url) {
		window.location = new_url;
	};

	// borrowed from:
	// 		http://stackoverflow.com/a/21210643
	this.get_params = function() {
		var queryDict = {}
		if ( location.search != '' ) {
			location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
		} else {
			var parts = location.hash.split('?')
			parts[parts.length-1].split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
		}
		return queryDict;
	};

	// set the page that the login page should redirect to after success
	this.set_login_redirect_page = function(page_name) {
		localStorage.setItem("login_redirect_page", page_name);
	}

	// get the page that the login page should redirect to after success
	this.get_login_redirect_page = function() {
		return localStorage.getItem("login_redirect_page"); 
	}

	this.validate_inputs = function(prefix, invalid_class, fields) {
		var valid = true;
		for(var i=0; i<fields.length; i++) {
			var element_id = prefix + fields[i];
			$('#' + element_id).removeClass(invalid_class);
			var val = $('#' + element_id).val();
			var vtype = $('#' + element_id).attr('vtype');
			var type = vtype.split(',')[0];
			var _valid = true;
			switch(type) {
				case 'string':
					if ( val == null || typeof(val) == 'undefined' ) {
						_valid = false;
					}
					if( vtype.split(',').length == 2 && vtype.split(',')[1] == 'required' && val == '' ) {
						_valid  = false;
					}
					break;
				case 'phone':
					// todo: regex this
					if ( val == null || typeof(val) == 'undefined' )
						_valid = false;
					break;
				case 'integer':
					if( vtype.split(',').length != 3 ) {
						console.log('Utils.validate_inputs(), warning!  missing integer ranges: ', vtype);	
						min = 0;
						max = 9007199254740991; // max value for int
					} else {
						var min = vtype.split(',')[1];
						var max = vtype.split(',')[2];
						if( isNaN(parseInt(min)) || isNaN(parseInt(max)) || isNaN(parseInt(val)) ) {
							console.log('first invalid');
							_valid = false;
						} else if ( parseInt(val) < parseInt(min) || parseInt(val) > parseInt(max) ) {
							console.log('second invalid', val, min, max);
							_valid = false;
						}
					}
					break;
				case 'email':
					// todo: regex this
					if ( val == null || typeof(val) == 'undefined' ) {
						_valid = false;
					}
					if( vtype.split(',').length == 2 && vtype.split(',')[1] == 'required' && val == '' ) {
						_valid  = false;
					}
					break;
				case '':
				default:
					console.log('Utils.validate_inputs(), error!  unknown vtype: ', vtype);
					break;
			};

			if ( !_valid ) {
				$('#' + element_id).addClass(invalid_class);
				valid = false;
			}

			$('#' + element_id).on('keyup', function() {
				$(this).removeClass(invalid_class);
			});

			$('#' + element_id).on('mouseup', function() {
				$(this).removeClass(invalid_class);
			})
		}

		return valid;
	};

	this.generate_password = function(len) {
	    var text = "";
	    var possible = "abcdefghijklmnopqrstuvwxyz0123456789";
	    for( var i=0; i < len; i++ )
	        text += possible.charAt(Math.floor(Math.random() * possible.length));
	    return text;
	};

	// constructor
	this.init = function() {

	};

	// entry point
	return this.init();

};