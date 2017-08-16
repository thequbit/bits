
//
// This object has helpers for loggin in, logging out, and checking logged-in state.
//
var Auth = function() {

	this._user = null;

	this.login = function(email, password, callback) {
		var that = this;
		$.ajax({
			url: '/api/v1/users/_login',
			type: 'POST',
			data: JSON.stringify({
				email: email,
				password: $.sha256(password),
			}),
			success: function(resp) {
				var utils = new Utils();
				if( utils.valid_callback(callback) ) {
					callback(true, resp)
				}
			},
			error: function(resp) {
				var utils = new Utils();
				if( utils.valid_callback(callback) ) {
					callback(false, resp)
				}
			}
		});
	};

	this.change_password = function(user_id, new_password, callback) {
		$.ajax({
			url: '/api/v1/users/' + user_id + '/_change_password',
			type: 'PUT',
			data: JSON.stringify({
				new_password: new_password
			}),
			success: function(resp) {
					callback(true, resp);
			},
			error: function(resp) {
				callback(false, resp);
			}
		});
	};

	this.is_logged_in = function(callback) {
		console.log('typeof(callback): ', typeof(callback));
		var utils = new Utils();
		var that = this;
		$.ajax({
			url: '/api/v1/users/_login?',// + utils.build_token_param(),
			type: 'GET',
			success: function(resp) {
				//console.log('typeof(callback): ', typeof(callback));
				//console.log('Auth.is_logged_in(), success: ', resp);
				var utils = new Utils();
				//if( utils.valid_callback(callback) ) {
				if( typeof(callback) == 'function' ) {
					//console.log()
					if ( resp.loggedin ) {
						console.log('auth.is_logged_in(), logged in.');
						callback(true, resp.user)
					} else {
						console.log('auth.is_logged_in(), not logged in.');
						callback(false, resp);
						//callback(true, resp);

					}
				} else {
					console.log('invalid callback', callback);
				}
				
			},
			error: function(resp) {
				//console.log('Auth.is_logged_in(), error: ', resp);
				var utils = new Utils();
				if( utils.valid_callback(callback) ) {
					callback(false, resp);
				}
			}
		});
	};

	this.logout = function(callback) {
		$.ajax({
			url: '/api/v1/users/_logout',
			type: 'POST',
			data: JSON.stringify({}),
			success: function(resp) {
				var utils = new Utils();
				if( utils.valid_callback(callback) ) {
					callback(true, resp)
				}
			},
			error: function(resp) {
				var utils = new Utils();
				if( utils.valid_callback(callback) ) {
					callback(false, resp);
				}
			}
		});
	};

	// constructor
	this.init = function() {

	};

	// entry point
	return this.init();

};