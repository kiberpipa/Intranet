<?php
	define('DJANGO_DB', 'i3');
	define('DJANGO_DB_HOST', '127.0.0.1');
	define('DJANGO_DB_PORT', '5433');
	define('DJANGO_USER', 'dokuwiki_intranet');
	define('DJANGO_PASS', 'ery5yredf593$!!=');
	define('DJANGO_SECRET', 'ok_=+nmxlxjjib&nf=t)qa6a*bb#6wwxvnygjyt7*%vp5j+)fk');
	define('DJANGO_LOGOUT_URL', 'https://www.kiberpipa.org/intranet/accounts/logout/?next=/intranet/wiki/');
	/**
	* django auth backend
	*
	* Uses external Trust mechanism to check against a django session id
	*
	* @author	Andreas Gohr <andi@splitbrain.org>
	* @author	Michael Luggen <michael.luggen at rhone.ch>
	* Postgresql rewrite by Gasper Zejn.
	*/
	/* SQL functions to be set-up on server:

CREATE FUNCTION django_check_password(username TEXT, passwd TEXT)
RETURNS boolean AS $$
    SELECT encode(digest(salt || $2, type), 'hex') = hash as password_ok from (SELECT substring(password from E'^([^\$]+)') as type, substring(password from E'[\$]([^\$]+)[\$]') as salt, substring(password from E'[\$]([^\$]+)$') as hash from auth_user where username=$1 limit 1) as pas;
    $$
    LANGUAGE SQL;

CREATE LANGUAGE plpythonu;

CREATE FUNCTION django_get_session_user_id(session_data TEXT)
  RETURNS integer
AS $$
    import pickle
    if session_data is None:
        return None
    data = pickle.loads(session_data.decode('string_escape').decode('string_escape'))
    return data.get('_auth_user_id', None)
$$ LANGUAGE plpythonu;


CREATE FUNCTION django_get_session_user (session_key TEXT, django_secret TEXT)
RETURNS integer
AS $$
    SELECT user_id from (SELECT django_get_session_user_id(substring(decoded from 0 for decoded_length - 31) :: text) as user_id, substring(decoded from decoded_length - 31) as tamper_check, encode(digest(substring(decoded from 0 for decoded_length - 31) || $2, 'md5'), 'hex') as tamper_hash FROM (SELECT session_key, decode(session_data, 'base64') as decoded, length(decode(session_data, 'base64')) as decoded_length from django_session where session_key = $1 AND expire_date > NOW() LIMIT 1) AS decoder) AS checker;
$$ LANGUAGE SQL;

	*/
	
	define('DOKU_AUTH', dirname(__FILE__));
	define('AUTH_USERFILE',DOKU_CONF.'users.auth.php');
	
	class auth_django extends auth_basic {
	
	/**
	* Constructor.
	*
	* Sets additional capabilities and config strings
	*/
	function auth_django(){
		$this->cando['external'] = true;
		$this->cando['logoff'] = true;
	}
	
	/**
	* Just checks against the django sessionid variable
	*/
	function trustExternal($user,$pass,$sticky=false){
		global $USERINFO;
		global $conf;
		$sticky ? $sticky = true : $sticky = false; //sanity check
		
		if( isset($_COOKIE['sessionid'])){
			
			/**
			 * get user info from django-database (only mysql at the moment)
			 */
			
			$s_id =  $_COOKIE['sessionid'];
			
			// Connecting, selecting database
			$conn = pg_connect('host=' . DJANGO_DB_HOST . ' port=' . DJANGO_DB_PORT . ' dbname=' . DJANGO_DB . ' user=' . DJANGO_USER . ' password=' . DJANGO_PASS) or die("Could not connect to database.");
			
			// Performing SQL query
			$query = pg_query($conn, "SELECT django_get_session_user('" . pg_escape_string($s_id) . "','" . pg_escape_string(DJANGO_SECRET). "')") or die("Could not execute query." . pg_last_error($conn)); 
			
			$result = pg_fetch_all($query);
			
			if ($result[0]['django_get_session_user']) {
				// if we have an user id then it's logged in
				
				$userquery = pg_query($conn, "SELECT username, first_name, email FROM auth_user WHERE id=" . $result[0]['django_get_session_user']) or die("Could not fetch user from DB.");
				
				$user = pg_fetch_all($userquery);
				
				$username = $user[0]['username'];
				$userfullname = $user[0]['first_name'];
				$useremail = $user[0]['email'];
				
				pg_free_result($query);
				pg_free_result($result);
				pg_free_result($userquery);
				pg_free_result($user);
				pg_close($conn);
				
				$groups = $this->_getUserGroups($username);
				
				$USERINFO['name'] = $username;
				$USERINFO['pass'] = '';
				$USERINFO['mail'] = $useremail;
				
				// Hack for a standard group
				$groups[0] = 'user';
				
				$USERINFO['grps'] = $groups;
				
				$_SERVER['REMOTE_USER'] = $username;
				
				$_SESSION[$conf['title']]['auth']['user'] = $username;
				$_SESSION[$conf['title']]['auth']['info'] = $userfullname;
				return true;
			}
		}
		$USERINFO['grps'] = Array(0 => 'ALL');
		return false;
	}
	
	function logOff() {
		header("Location: " . DJANGO_LOGOUT_URL);
		exit();
	}
	
	function _getUserGroups($user){
		if(!@file_exists(AUTH_USERFILE)) return;
		
		$lines = file(AUTH_USERFILE);
		foreach($lines as $line){
			$line = preg_replace('/#.*$/','',$line); //ignore comments
			$line = trim($line);
			if(empty($line))
				continue;
			$row = split(":",$line,5);
			$groups = split(",",$row[4]);
			
			if($user == $row[0])
				return $groups;
		}
		return;
		}
	}
?>
