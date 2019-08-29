
 `define ITEM2
`timescale 1ns/10ps


`ifdef ITEM1
`include "tb1.v"
`endif

`ifdef ITEM2
`include "tb2.v"
`endif

`ifdef ITEM3
`include "tb3.v"
`endif

`ifdef ITEM4
`include "tb4.v"
`endif