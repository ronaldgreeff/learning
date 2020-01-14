/* If / else statements */

var firstName = 'John';
var age = 16;

if (age < 13) {
	console.log(firstName + ' is a boy.');
} else if (age >= 13 && age < 20) { // between 13 and 20 // age >= 13 AND age < 20
	console.log(firstName + ' is a teen.');
} else if (age >= 20 && age < 30) {
	console.log(firstName + ' is a young man.');
} else {
	console.log(firstName + ' is a man.');
}

/*
Truth table
AND (&&)   => 	true if ALL are true / false if ONE is false
	1 >= 2 && 1 < 3 = false
OR (||)	   => 	true if ONE is true / false if ALL are false
	1 >= 2 || 1 < 3 = false
NOT (!)	   => 	inverts true/false value
*/