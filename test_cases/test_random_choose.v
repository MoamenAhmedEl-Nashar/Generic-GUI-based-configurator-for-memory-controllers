`timescale 1ns/1ns


/*
test bench for testing random choose module
*/
module test_choose ;
/*j*/ 
 parameter WIDTH = 10 , x = 4; /*h*/
 /*h*/ 
 parameter WIDTH2 = 2;
 parameter WIDTH3 = 31; // modify if ...
 parameter WIDTH4 = 31;
 // modify if ...
 parameter WIDTH5 = 31;
 parameter WID = 100;
 parameter WIDTH6 = 31;
 parameter WIDTH7 = 31;
 parameter WIDTH8 = 31;
 parameter WIDTH9 = 31;
 parameter WIDTH10 = 31;
 parameter WIDTH11 = 31;
 parameter WIDTH12 = 31;
 parameter WIDTH13 = 31;
 parameter WIDTH14 = 31;
 parameter WIDTH15 = 31;
 parameter WIDTH16 = 31;
 parameter WIDTH17 = 31;
 parameter WIDTH18 = 31;
 parameter WIDTH19 = 31;
 parameter WIDTH20 = 31;
 parameter WIDTH21 = 31;
 parameter WIDTH22 = 31;
 parameter WIDTH23 = 31;

 // Inputs
 reg clock;
 reg reset;
 reg enable;
 reg [WIDTH:0]weight0,weight1,weight2,weight3;
 reg [WIDTH:0]seed;
 
 // Outputs
 wire  [1:0] out_segment_number;
 
 // Instantiate the Unit Under Test (UUT)
 RandomChoose  #(.WIDTH(WIDTH))uut (
  .in_clock(clock), 
  .in_reset(reset),
  .in_enable(enable),
  .in_weight0(weight0),
  .in_weight1(weight1),
  .in_weight2(weight2),
  .in_weight3(weight3),
  .in_seed(seed), 
  .out_segment_number(out_segment_number)
 );
  
 initial begin
  clock = 0;
  forever
   #50 clock = ~clock;
  end
   
 initial begin
  // Initialize Inputs
  ////////////////
  weight0 = 2;
  weight1 = 4;
  weight2 = 2;
  weight3 = 0;
  ///////////////
  reset = 0;
  enable = 0;
  // Wait 100 ns for global reset to finish
  #100;
      seed = 1;
      reset = 1;
      enable = 1;
  #200;
  reset = 0;
  #100
  enable=0;
  #200
  enable=1;
  #500
  enable=0;
  #300
  enable=1;
 
  
 end
  
 initial begin
 $display("out_segment_number");
 //$monitor("%d", out_segment_number);
 end     


integer count0=0;
integer count1=0;
integer count2=0;
integer count3=0;
 always @(posedge clock)
 begin
    $monitor("count of segment 0 is %d",count0);
    $monitor("count of segment 1 is %d",count1);
    $monitor("count of segment 2 is %d",count2);
    $monitor("count of segment 3 is %d",count3);

   if(out_segment_number==0)
   begin
     count0=count0+1;
   end
   if(out_segment_number==1)
   begin
     count1=count1+1;
   end
   if(out_segment_number==2)
   begin
     count2=count2+1;
   end
   if(out_segment_number==3)
   begin
     count3=count3+1;
   end
 end
endmodule
