package com.example.bica

import enumextensions.EnumMirror

class MoralSchemaDef[R: EnumMirror, FabulaNode](
  tryBind: (Seq[Actor], Seq[R]) => Seq[MoralSchema[R, FabulaNode]],
  fabula: Fabula[R, FabulaNode],
  objectives: Map[R, Any]
) {
    val roles: IArray[R] = EnumMirror[R].values
}
