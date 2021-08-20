/*



  parameter int pW = 36;
  parameter int pA = 18;



  logic          example_module__irst     ;
  // Clock signals
  logic          example_module__iclk     ;
  logic          example_module__iclk_ena ;
  // Data bus signals
  logic          example_module__owrena   ;
  logic          example_module__ordena   ;
  logic [pA-1:0] example_module__owr_adr  ;
  logic [pA-1:0] example_module__ord_adr  ;
  logic [pW-1:0] example_module__odat     ;
  logic          example_module__iena     ;
  logic [pW-1:0] example_module__idat     ;



  example_module
  #(
    . pW    (pW      ) ,
    . pA    (pA      ) 
  )
  example_module__
  (
    .irst     (example_module__irst          ) ,
    // Clock signals
    .iclk     (example_module__iclk          ) ,
    .iclk_ena (example_module__iclk_ena      ) ,
    // Data bus signals
    .owrena   (example_module__owrena        ) ,
    .ordena   (example_module__ordena        ) ,
    .owr_adr  (example_module__owr_adr       ) ,
    .ord_adr  (example_module__ord_adr       ) ,
    .odat     (example_module__odat          ) ,
    .iena     (example_module__iena          ) ,
    .idat     (example_module__idat          ) 
  );


  assign example_module__irst     = '0;
  assign example_module__iclk     = '0;
  assign example_module__iclk_ena = '0;
  assign example_module__iena     = '0;
  assign example_module__idat     = '0;



*/ 



module example_module
#(
  parameter int pW = 36 ,
  parameter int pA = 18 
)
(
  irst     ,
  // Clock signals
  iclk     ,
  iclk_ena ,
  // Data bus signals
  owrena   ,
  ordena   ,
  owr_adr  ,
  ord_adr  ,
  odat     ,
  iena     ,
  idat     
);

  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------

  localparam int pLOCAL = 22;

  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------

  input  logic          irst     ;
  // Clock signals
  input  logic          iclk     ;
  input  logic          iclk_ena ;
  // Data bus signals
  output logic          owrena   ;
  output logic          ordena   ;
  output logic [pA-1:0] owr_adr  ;
  output logic [pA-1:0] ord_adr  ;
  output logic [pW-1:0] odat     ;
  input  logic          iena     ;
  input  logic [pW-1:0] idat     ;

  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------


  //------------------------------------------------------------------------------------------------------
  //
  //------------------------------------------------------------------------------------------------------



endmodule
