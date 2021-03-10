import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: topButton
    property url btnIconSource: "../../Images/svg_images/minimize_icon.svg"
    property color colorDefault: "#000000"
    property color colorMouseOver: "#2e3836"
    property color colorPressed: "#a30000"
    QtObject{
        id: internal

        property var dynamicColor: if(topButton.down){
                                       topButton.down ? colorPressed : colorDefault
                                   }else{
                                       topButton.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitWidth: 50
    implicitHeight: 50
    background: Rectangle{
        id: bgBtn
        color: internal.dynamicColor

        Image{
            id: iconBtn
            source: btnIconSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 16
            width: 16
            fillMode: Image.PreserveAspectFit
        }
        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#f5f5f5"
            antialiasing: false
        }
    }
}

