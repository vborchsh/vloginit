/*



  parameter int pW = 36;
  parameter int pA = 18;



  logic          exmaple_module__irst     ;
  // Clock signals
  logic          exmaple_module__iclk     ;
  logic          exmaple_module__iclk_ena ;
  // Data bus signals
  logic          exmaple_module__owrena   ;
  logic          exmaple_module__ordena   ;
  logic [pA-1:0] exmaple_module__owr_adr  ;
  logic [pA-1:0] exmaple_module__ord_adr  ;
  logic [pW-1:0] exmaple_module__odat     ;
  logic          exmaple_module__iena     ;
  logic [pW-1:0] exmaple_module__idat     ;



  exmaple_module
  #(
    . pW    (pW      ) ,
    . pA    (pA      ) 
  )
  exmaple_module__
  (
    .irst     (exmaple_module__irst          ) ,
    // Clock signals
    .iclk     (exmaple_module__iclk          ) ,
    .iclk_ena (exmaple_module__iclk_ena      ) ,
    // Data bus signals
    .owrena   (exmaple_module__owrena        ) ,
    .ordena   (exmaple_module__ordena        ) ,
    .owr_adr  (exmaple_module__owr_adr       ) ,
    .ord_adr  (exmaple_module__ord_adr       ) ,
    .odat     (exmaple_module__odat          ) ,
    .iena     (exmaple_module__iena          ) ,
    .idat     (exmaple_module__idat          ) 
  );


  assign exmaple_module__irst     = '0;
  assign exmaple_module__iclk     = '0;
  assign exmaple_module__iclk_ena = '0;
  assign exmaple_module__iena     = '0;
  assign exmaple_module__idat     = '0;



*/ 



module exmaple_module
#(
  parameter int pW = 36 ,
  parameter int pA = 18 
)
(
  input  logic          irst     ,
  // Clock signals
  input  logic          iclk     ,
  input  logic          iclk_ena ,
  // Data bus signals
  output logic          owrena   ,
  output logic          ordena   ,
  output logic [pA-1:0] owr_adr  ,
  output logic [pA-1:0] ord_adr  ,
  output logic [pW-1:0] odat     ,
  input  logic          iena     ,
  input  logic [pW-1:0] idat     
);

  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------

  localparam int pLOCAL = 22;

  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------


  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------


  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------



endmodule
