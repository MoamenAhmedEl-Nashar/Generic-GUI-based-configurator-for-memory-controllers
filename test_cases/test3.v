
 

`include "param.v"
module test;

parameter any = 1;
  `ifdef VPS_FLOW
   vps_lpddr5_sm
  `else veloce_lpddr5_sm `endif 

    #(.DENSITY (DENSITY_CODE)) uut (
  .in_clock(clock), 
  .in_reset(reset),
  .out_segment_number(out_segment_number)
 );
endmodule