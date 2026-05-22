from agents_ai.crew import SecurityCrew

code_bundle = """
import React, { useState } from 'react'

export interface ButtonProps {
    children?: React.ReactNode;
    name?: string;
    leftName?: string;
    rightName?: string;
    bgColor?: string;
    borderColor?: string;
    borderWidth?: string;
    hoverBgColor?: string;
    hoverTextColor?: string;
    hoverBorderColor?: string;
    width: string;
    height: string;
    textSize: string;
    fontSize?: string;
    textColor?: string;
    svgLeft?: string | React.ReactNode;
    svgRight?: string | React.ReactNode;
}

function Maintbutton({ children, name, leftName, rightName, bgColor, borderColor, borderWidth, hoverBgColor, hoverTextColor, hoverBorderColor, width, height, textSize, fontSize, textColor, svgLeft, svgRight }: ButtonProps) {
    const [hovered, setHovered] = useState(false)

    const resolvedFontSize = textSize?.replace('text-', '') === 'base' ? '1rem'
        : textSize?.replace('text-', '') === 'sm' ? '0.875rem'
        : textSize?.replace('text-', '') === 'lg' ? '1.125rem'
        : textSize?.replace('text-', '') === 'xl' ? '1.25rem'
        : undefined

    return (
        <button
            className={`group flex items-center justify-center gap-2 rounded-sm px-4 py-2 ${fontSize ? `font-${fontSize}` : ''}`}
            style={{
                backgroundColor: hovered ? (hoverBgColor ?? 'transparent') : (bgColor ?? undefined),
                color: hovered ? (hoverTextColor ?? (bgColor ?? textColor)) : (textColor ?? undefined),
                borderColor: hovered ? (hoverBorderColor ?? borderColor) : (borderColor ?? undefined),
                borderWidth: borderWidth ? `${borderWidth}px` : undefined,
                borderStyle: borderColor ? 'solid' : undefined,
                width: width ? `${width === '52' ? '13rem' : width}` : undefined,
                height: height ? `${height === '8' ? '2.5rem' : height}` : undefined,
                fontSize: resolvedFontSize,
                transition: 'background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease',
            }}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
        >
            {svgLeft && <span className="transition-transform duration-200 group-hover:-translate-x-0.5">{svgLeft}</span>}
            {name || children}
            {svgRight && <span className="transition-transform duration-200 group-hover:translate-x-1">{svgRight}</span>}
        </button>
    );
}


export default Maintbutton

"""

inputs = {
    "repo_url": "local_analysis",
    "code_bundle": code_bundle,
}

SecurityCrew().crew().kickoff(inputs=inputs)
