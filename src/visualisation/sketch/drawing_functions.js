function drawVectorField() {
  var yoff = 0;
  for (let y=0; y < rows; y++) {
    var angle;
    var xoff = 0;
    for (let x=0; x < cols; x++) {
      var index = x + y * cols;
      //let anglesAndDistances = setEachScaledPixelAngle_calculateAlltheDistancesToEachSkeletonKeyPoint(x, y);
      let anglesAndDistances = setEachScaledPixelAngle_calculateOneLimbtheDistancesToEachSkeletonKeyPoint(x, y);
      let angles = anglesAndDistances.angles;
      let distances = anglesAndDistances.distances;
      distances = Object.keys(distances).map(function(key){
          return distances[key];
      });
      angles = Object.keys(angles).map(function(key){
          return angles[key];
      });
      
      var angles_list = [];
      for (let i=0; i<angles.length; i++) {
        let dist_val_for_angles_list = calculateCoefForEachVectorsAngle(angles[i], distances[i], calculateSum(distances));
        //let movement_distances_values = Object.keys(movement_distances).map(function(key){ return movement_distances[key]; });
        //let ampl_val_for_angles_list = calculateCoefForEachVectorsAngle(angles[i], movement_distances_values[i], calculateSum(movement_distances_values));
        
        angles_list[i] = calculateAnglesList(angles[i], distances[i], 0, dist_val_for_angles_list, 0, flagWithAmplitude=false); // only distance as a weight
        //angles_list[i] = calculateAnglesList(angles[i], distances[i], movement_distances_values[i], dist_val_for_angles_list, ampl_val_for_angles_list, flagWithAmplitude=true); // distance & amplitude as a weight
      }
      // this sum of angles is already weighted by the distances 
      angle = calculateSum(angles_list) * noise(xoff, yoff, zoff);
      var v = p5.Vector.fromAngle(angle);
      //drawVectors(v, x, y, scl, 'black');
      drawPariclesMovingOnTopOfFlowField(v, index);
      xoff += inc;
    }
    yoff += inc;
    zoff += 0.5;
  }
}

function drawPariclesMovingOnTopOfFlowField(v, index) {
  v.setMag(1);
  gr.stroke('black');
  flowfield[index] = v;
}

function drawVectors(v, x, y, scl, myColor) {
  gr.stroke(myColor);
  push();
  gr.translate(x * scl, y * scl);
  gr.rotate(v.heading());
  gr.line(0, 0, scl, 0);
  //let arrowSize = 1;
  //translate(0, 0);
  //triangle(0, arrowSize / 2, 0, -arrowSize / 2, arrowSize, 0);
  pop();
}

function drawRedSkeletonVectors() {
  for (let y=0; y < rows; y++) {
    let angle;
    for (let x=0; x < cols; x++) {
      for(let key in skeleton_angles) {
        //print('a key from skeleton angles: ', key);
        if (key == String([x, y])) {
          angle = skeleton_angles[key];
          let v = p5.Vector.fromAngle(angle);
          drawVectors(v, x, y, scl, 'red');
        }
      }
    }
  }
}

//function drawArrow(base, v, myColor) {
//  push();
//  stroke(myColor);
//  strokeWeight(1);
//  fill(myColor);
//  translate(base.x, base.y);
//  line(0, 0, vec.x, vec.y);
//  rotate(v.heading());
//  let arrowSize = 3;
//  translate(v.mag() - arrowSize, 0);
//  triangle(0, arrowSize / 2, 0, -arrowSize / 2, arrowSize, 0);
//  pop();
//}
