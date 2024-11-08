ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "3.5.2"

lazy val root = (project in file("."))
    .settings(
        name := "scala",
        idePackagePrefix := Some("com.example.bica")
    )
    libraryDependencies += "io.github.bishabosha" %% "enum-extensions" % "0.1.1"
