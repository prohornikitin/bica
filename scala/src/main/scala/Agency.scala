package com.example.bica

import enumextensions.EnumMirror

case class Agency[R : EnumMirror](
  perspective: R,
  objectiveCheck: Actor => Boolean,
  //TODO: mood
)
