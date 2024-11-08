package com.example.bica

import utils.{Feelings, FeelingsImmutable}

import enumextensions.EnumMirror

import scala.collection.immutable.Seq

type Condition[R] = Seq[Map[R, Actor]] => Boolean

case class Fabula[R : EnumMirror, Node](
    story: Seq[Node] = Seq.empty[Node],
    connections: Map[Node, (Condition[R], Node)] = Map.empty[Node, (Condition[R], Node)],
)
