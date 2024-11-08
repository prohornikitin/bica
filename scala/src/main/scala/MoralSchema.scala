package com.example.bica

import enumextensions.EnumMirror


case class MoralSchema[R: EnumMirror, FabulaNode](
  interface: Interface[R],
  fabula: Fabula[R, FabulaNode],
  agency: Agency[R],
)