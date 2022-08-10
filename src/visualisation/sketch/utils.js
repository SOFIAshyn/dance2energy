function setSkeletonArrays() {
  for (let y=0; y<rows; y++) {
    let angle;
    for (let x=0; x < cols; x++) {
      for(let key in skeleton_angles) {
        if (key == String([x, y])) {
          angle = skeleton_angles[key];
        }
      }
    }
  }
}

function setEachScaledPixelAngle_calculateAlltheDistancesToEachSkeletonKeyPoint(x, y) {
  let angles = [];
  let distances = [];
  for (let key in skeleton_angles) {
    let key_x = parseInt(key.split(",")[0]);
    let key_y = parseInt(key.split(",")[1]);
    let dist = getDistance(key_x, key_y, x, y);
    let skeleton_index = skeleton_keypoints_numbers[key];
    angles[skeleton_index] = skeleton_angles[key];
    if (dist == 0) {
      distances[skeleton_index] = 0;
    } else {
      distances[skeleton_index] = 1/dist;
    }
  }
  return {'angles': angles, 'distances': distances};
}

function get_coef_for_dist_weighted_val(distances) {
  let sum_distances = calculateSum(distances);
  return 1/sum_distances;
}

function setEachScaledPixelAngle_calculateOneLimbtheDistancesToEachSkeletonKeyPoint(x, y) {
  let angles = [];
  let distances = [];
  for (let key in skeleton_angles) {
    let key_x = parseInt(key.split(",")[0]);
    let key_y = parseInt(key.split(",")[1]);
    let dist = getDistance(key_x, key_y, x, y);
    let skeleton_index = skeleton_keypoints_numbers[key];
    angles[skeleton_index] = skeleton_angles[key];
    if (dist == 0) {
      distances[skeleton_index] = 0;
    } else {
      distances[skeleton_index] = dist;
    }
  }
  // count only the limb that is the closest - set other distances to zero
  var body_sum_dict = {};
  for (var i = 0; i < arr_of_parts.length; i++) {
    let body_values = arr_of_parts[i];
    let body_key = arr_of_parts_num[i];
    //print('body_key = ', body_key);
    //print('body_values = ', body_values);
    var dist_sum = 0;
    for (var j = 0; j < body_values.length; j++) {
      for (const [dist_key, dist_value] of distances.entries()) {
        //print('dist_key = ', dist_key, '; dist_value = ', dist_value);
        //print('body_values[j] = ', j, body_values[j]);
        //print('dist_key = ', dist_key);
        if (body_values[j] == dist_key) {
          //print('to ', dist_sum, 'adding ', dist_value);
          if (isNaN(dist_value) == false) { dist_sum += dist_value; }
          //print('body_values[j], dist_key, dist_value = ', body_values[j], dist_key, dist_value, dist_sum);
        }
      }
    }
    body_sum_dict[body_key] = dist_sum;
    //print('for this ', body_key, 'we have this sum = ', dist_sum);
  }
  //print('body_sum_dict = ', body_sum_dict);
  //print('body_sum_dict = ', body_sum_dict);
  //let body_part_to_count = min(body_sum_dict, key=body_sum_dict.get);
  let body_part_to_count = Object.keys(body_sum_dict).reduce((key, v) => body_sum_dict[v] < body_sum_dict[key] ? v : key);
  //print('we are choosing: ', body_part_to_count);
  let dist_to_one_limb = {};
  //print('body_part_to_count = ', body_part_to_count);
  for (const [dist_key, dist_value] of distances.entries()) {
    let indx_of_values = arr_of_parts_num_inv[body_part_to_count];
    let body_part_values = arr_of_parts[indx_of_values];
    if (body_part_values.includes(dist_key) == false || isNaN(dist_value)) {
      dist_to_one_limb[dist_key] = 0;
    } else {
      dist_to_one_limb[dist_key] = 1/dist_value;
    }
  }
  return {'angles': angles, 'distances': dist_to_one_limb};
}

function calculateSum(listToSumUp) {
  return listToSumUp.reduce((partialSum, a) => partialSum + a, 0);
}

function calculateAnglesList(angle, distance, movement_distances_value, dist_val_for_angles_list,  ampl_val_for_angles_list, flagWithAmplitude) {
  if (flagWithAmplitude == false) {
    //print('angle, distance, dist_val_for_angles_list = ', angle, distance, dist_val_for_angles_list);
    // dist_val_for_angles_list = angleOfKeyPoint * (1/dist_sum) * invDistanceOfKeyPoint;
    return angle * dist_val_for_angles_list;
  }
  let dist_coef = 0.8;
  let amplitude_coef = 0.2;
  return angle * (dist_val_for_angles_list*dist_coef + ampl_val_for_angles_list*amplitude_coef);
}

function getDistance(x1, y1, x2, y2){
    let y = x2 - x1;
    let x = y2 - y1;
    return Math.sqrt(x * x + y * y);
}

function calculateCoefForEachVectorsAngle(angleOfKeyPoint, invDistanceOfKeyPoint, dist_sum) {
  // arguments: angles[i], distances[i], dist_sum
  // dist handle NaN
  let dist_val_for_angles_list = angleOfKeyPoint * (1/dist_sum) * invDistanceOfKeyPoint;
  if (isNaN(dist_val_for_angles_list)) {
    dist_val_for_angles_list = 0;
  }
  return dist_val_for_angles_list;
}

function defineVectors(final_list_prev_x, final_list_prev_y, final_list_cur_x, final_list_cur_y) {
  //print('we are in function: defineVectors');
  //print('skeleton_points = ', skeleton_points);
  for (let i=0; i<skeleton_points; i++) {
    print('i = ', i);
    // i - an number of skeleton point
    //print(final_list_prev_x[0]);
    let row_prev = getVectorPixel(final_list_prev_x[i]);
    let col_prev = getVectorPixel(final_list_prev_y[i]);
    
    let row_cur = getVectorPixel(final_list_cur_x[i]);
    let col_cur = getVectorPixel(final_list_cur_y[i]);
    
    angle = defineAngle(col_prev, col_cur, row_prev, row_cur);
    
    let cell = define_non_conflict_cell(row_prev, col_prev, skeleton_angles);
    skeleton_angles[cell] = angle;
    skeleton_keypoints_numbers[cell] = i;
    print('to ', cell, ' added ', i);
  }
  print('skeleton_angles = ', skeleton_angles);
  print('skeleton_keypoints_numbers = ', skeleton_keypoints_numbers);
  //str = JSON.stringify(skeleton_angles, null, 4); // (Optional) beautiful indented output.
  //print(str);
}

function define_non_conflict_cell(row_prev, col_prev, skeleton_angles) {
  let cell = String([row_prev, col_prev]);
  print('cell = ', cell, ' in ', skeleton_angles);
  //print(cell)
  if (cell in skeleton_angles) {
    cell = String([row_prev+1, col_prev+1]);
  }
  if (cell in skeleton_angles) {
    cell = String([row_prev-1, col_prev+1]);
  }
  if (cell in skeleton_angles) {
    cell = String([row_prev+1, col_prev-1]);
  }
  if (cell in skeleton_angles) {
    cell = String([row_prev-1, col_prev-1]);
  }
  return cell;
}

function defineAngle(col_prev, col_cur, row_prev, row_cur) {
  //print('col_prev = ', col_prev, 'col_cur = ', col_cur, 'row_prev = ', row_prev, 'row_cur = ', row_cur);
  let v0 = createVector(col_prev, row_prev);
  let v1 = createVector(col_cur, row_cur);
  
  if (col_prev > col_cur) { // down on y axis
    if (row_prev < row_cur) { // right on x axis
      angle = PI/4;
    }
    if (row_prev == row_cur) {
      angle = PI/2;
    }
    if (row_prev > row_cur) { // left on x axis
      angle = 3*PI/4;
    }
  }
  if (col_prev == col_cur) { // on one line
    if (row_prev < row_cur) { // right 
      angle = 0;
    }
    if (row_prev == row_cur) {
      angle = 0; // nothing
    }
    if (row_prev > row_cur) { // left
      angle = PI;
    }
  }
  if (col_prev < col_cur) { // up on y axis
    if (row_prev < row_cur) { // right on x axis
      angle = 7*PI/4;
    }
    if (row_prev == row_cur) { 
      angle = 3*PI/2;
    }
    if (row_prev > row_cur) { // left
      angle = 5*PI/4;
    }
  }
  
  //print('the result angle is = ', angle);
  return angle;
}

function getVectorPixel(val) {
  const res = floor(val/scl);
  //print('res = ', res);
  return res;
}
