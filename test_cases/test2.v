
 `define USE_WREAL
`include "params.v"

module dut (
  parameter enable = 2,

  `ifdef USE_WREAL
  parameter real = 2,
  `else
  parameter vddc = 2,
  `endif
  input vddf,

  output [31:0] port_a,
  output [15:0] port_b
);
  always @(*) begin
    // To expose a bug extracting pins when wreal support was added
  end
endmodule