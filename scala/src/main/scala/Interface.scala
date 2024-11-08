package com.example.bica

import enumextensions.EnumMirror



case class Interface[R: EnumMirror](
  actors: Map[R, Actor]
    //TODO??: условия применимости
)
