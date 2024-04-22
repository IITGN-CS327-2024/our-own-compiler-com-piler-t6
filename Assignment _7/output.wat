(module
(global $x (mut i32) 
  (i32.const 0)
)  ; Initial dummy value
(func (export "init_x")
  (global.set $x 
    ; Unsupported node type: number
 ; Unsupported node type: number
 i32.add
))
)
