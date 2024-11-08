package com.example.bica

import enumextensions.EnumMirror

object Example {
    enum Roles derives EnumMirror {
        case Tutor
        case Student
    }


    val moralSchemaDef: MoralSchemaDef[Roles, String] = MoralSchemaDef[Roles, String](
        (a, b) => Seq.empty,
        Fabula(),
        Map.empty,
    )

}
