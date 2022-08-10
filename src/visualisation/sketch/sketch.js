// last updates: 20/05/2022
// NEXT STEPS: play with magnitude, with color

// variables for each video 
var frame_i = 36;
var index_of_video_in_list = 2;
var canvasHeight = 1920;
var canvasWidth = 1080;
// basic variables
var gr;
let num_of_frames;
let engine_generation_iteration_limit = 50;
var num_of_particles = 10000;
var cur_skeleton_name;
var prev_skeleton_name;
var final_list_prev_x;
var final_list_prev_y;
var final_list_cur_x;
var final_list_cur_y;

function preload() {
  let json_name = ('p5_'.concat(list_of_one_person_dancing_videos[index_of_video_in_list])).concat('.json');
  jsonFile = loadJSON('assets/'.concat(json_name));
}

function setup() {
  createCanvas(canvasHeight, canvasWidth);
  cols = floor(width / scl);
  rows = floor(height / scl);
  
  num_of_frames = Object.values(jsonFile).length;
}

function draw() {
    gr = createGraphics(canvasHeight, canvasWidth);
    gr.background(51);
    flowfield = new Array(cols * rows);
    for (let i = 0; i < num_of_particles; i++) {
      particles[i] = new Particle();
    }
    cur_skeleton_name = jsonFile[frame_i].cur_skeleton_name;
    prev_skeleton_name = jsonFile[frame_i].prev_skeleton_name;
    final_list_prev_x = jsonFile[frame_i].final_list_prev_x;
    final_list_prev_y = jsonFile[frame_i].final_list_prev_y;
    final_list_cur_x = jsonFile[frame_i].final_list_cur_x;
    final_list_cur_y = jsonFile[frame_i].final_list_cur_y;
    movement_distances = jsonFile[frame_i].distance_of_direction_vectors;
    defineVectors(final_list_prev_x, final_list_prev_y, final_list_cur_x, final_list_cur_y, movement_distances);
    
    for (let i_times_draw = 0; i_times_draw < engine_generation_iteration_limit; i_times_draw++) {
      print('i am drawing ', i_times_draw, ' time.');
      setSkeletonArrays();
      drawVectorField();
      //drawRedSkeletonVectors();
      for (var i = 0; i < particles.length; i++) {
        particles[i].follow(flowfield);
        particles[i].update();
        particles[i].edges();
        particles[i].show();
      }
      image(gr, 0, 0);
    }
    save(gr, cur_skeleton_name);
    gr.reset();
    frame_i++;
    //if (frame_i == num_of_frames) {
    //  noLoop();
    //}
    print('frame_i = ', frame_i);
}
