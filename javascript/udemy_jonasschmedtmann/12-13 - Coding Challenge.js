/*****************************
* CODING CHALLENGE 1

Mark and John are trying to compare their BMI (Body Mass Index), which is calculated using the formula:

BMI = mass / height^2 = mass / (height * height). (mass in kg and height in meter).

1. Store Mark's and John's mass and height in variables
2. Calculate both their BMIs
3. Create a boolean variable containing information about whether Mark has a higher BMI than John.
4. Print a string to the console containing the variable from step 3. (Something like "Is Mark's BMI higher than John's? true").
GOOD LUCK 😀

*/

function getBMI (mass, height) {
	return (mass / (height*=2));
};

function compareBMIAgainstMarks (markBMI, johnBMI) {
	return markBMI > johnBMI;
};

function message (comparisonResult) {
	if (comparisonResult) {
		return console.log("Marks BMI is higher than John's")
	} else {
		return console.log("Marks BMI is not higher than John's")
	};
};

var markMass = 80;
var markHeight = 1.76784;

var johnMass = 100;
var johnHeight = 1.8288;

var markBMI = getBMI(markMass, markHeight);
var johnBMI = getBMI(johnMass, johnHeight);

message(compareBMIAgainstMarks(markBMI, johnBMI));